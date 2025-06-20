import logging
from typing import List, Dict, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
import faiss
from rank_bm25 import BM25Okapi
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import CrossEncoder

class HybridRetriever:
    def __init__(self, 
                 dense_model_name: str = "sentence-transformers/instructor-xl",
                 sparse_model_name: str = "neuralmind/bert-base-portuguese-cased",
                 cross_encoder_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
                 dense_weight: float = 0.6,
                 sparse_weight: float = 0.4,
                 cache_ttl: int = 24,
                 similarity_threshold: float = 0.65):
        """
        Inicializa o Hybrid Retriever com modelos e configurações.
        
        Args:
            dense_model_name: Nome do modelo para embeddings densos
            sparse_model_name: Nome do modelo para tokenização esparsa
            cross_encoder_name: Nome do modelo para reranking
            dense_weight: Peso para o score denso (0-1)
            sparse_weight: Peso para o score esparso (0-1)
            cache_ttl: Tempo de vida do cache em horas
            similarity_threshold: Limite para similaridade de fallback
        """
        self.dense_weight = dense_weight
        self.sparse_weight = sparse_weight
        self.cache_ttl = timedelta(hours=cache_ttl)
        self.similarity_threshold = similarity_threshold
        self.embedding_cache = {}
        self.logger = logging.getLogger(__name__)
        
        # Inicialização dos modelos
        self._initialize_models(dense_model_name, sparse_model_name, cross_encoder_name)
        
    def _initialize_models(self, dense_model_name: str, sparse_model_name: str, cross_encoder_name: str):
        """Carrega todos os modelos necessários."""
        try:
            # Modelo de embeddings densos
            self.dense_model = AutoModel.from_pretrained(dense_model_name)
            self.dense_tokenizer = AutoTokenizer.from_pretrained(dense_model_name)
            
            # Tokenizador para recuperação esparsa (BM25)
            self.sparse_tokenizer = AutoTokenizer.from_pretrained(sparse_model_name)
            
            # Modelo para reranking
            self.reranker = CrossEncoder(cross_encoder_name)
            
            self.logger.info("Todos os modelos foram carregados com sucesso.")
        except Exception as e:
            self.logger.error(f"Falha ao carregar modelos: {str(e)}")
            raise

    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Obtém embedding para um texto, com cache.
        
        Args:
            text: Texto para embeddar
            
        Returns:
            Embedding numpy array
        """
        # Verifica cache
        if text in self.embedding_cache:
            cached_embedding, timestamp = self.embedding_cache[text]
            if datetime.now() - timestamp < self.cache_ttl:
                return cached_embedding
        
        # Gera novo embedding se não estiver em cache ou expirado
        try:
            inputs = self.dense_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            outputs = self.dense_model(**inputs)
            embedding = self._mean_pooling(outputs, inputs['attention_mask']).numpy()
            
            # Atualiza cache
            self.embedding_cache[text] = (embedding, datetime.now())
            return embedding
        except Exception as e:
            self.logger.error(f"Erro ao gerar embedding: {str(e)}")
            raise

    def _mean_pooling(self, model_output, attention_mask):
        """Pooling para obter embedding de frase a partir de tokens."""
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def _sparse_retrieval(self, query: str, documents: List[str], k: int = 5) -> List[Tuple[int, float]]:
        """
        Recuperação esparsa usando BM25.
        
        Args:
            query: Texto da consulta
            documents: Lista de documentos para buscar
            k: Número de resultados a retornar
            
        Returns:
            Lista de tuplas (índice, score)
        """
        try:
            # Tokenização
            tokenized_docs = [self.sparse_tokenizer.tokenize(doc) for doc in documents]
            tokenized_query = self.sparse_tokenizer.tokenize(query)
            
            # Cria modelo BM25
            bm25 = BM25Okapi(tokenized_docs)
            
            # Obtém scores
            scores = bm25.get_scores(tokenized_query)
            
            # Pega os top-k
            top_k_indices = np.argsort(scores)[-k:][::-1]
            return [(i, scores[i]) for i in top_k_indices]
        except Exception as e:
            self.logger.error(f"Erro no sparse retrieval: {str(e)}")
            return []

    def _dense_retrieval(self, query: str, document_embeddings: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
        """
        Recuperação densa usando similaridade de cosseno.
        
        Args:
            query: Texto da consulta
            document_embeddings: Embeddings dos documentos (np.array)
            k: Número de resultados a retornar
            
        Returns:
            Lista de tuplas (índice, score)
        """
        try:
            # Obtém embedding da query
            query_embedding = self._get_embedding(query)
            
            # Calcula similaridade de cosseno
            similarities = np.dot(document_embeddings, query_embedding.T).flatten()
            
            # Normaliza scores para 0-1
            similarities = (similarities + 1) / 2
            
            # Pega os top-k
            top_k_indices = np.argsort(similarities)[-k:][::-1]
            return [(i, similarities[i]) for i in top_k_indices]
        except Exception as e:
            self.logger.error(f"Erro no dense retrieval: {str(e)}")
            return []

    def retrieve(self, query: str, documents: List[str], k: int = 5, use_reranking: bool = True) -> List[Tuple[int, float, str]]:
        """
        Método principal para recuperação híbrida.
        
        Args:
            query: Texto da consulta
            documents: Lista de documentos para buscar
            k: Número de resultados a retornar
            use_reranking: Se deve aplicar reranking com cross-encoder
            
        Returns:
            Lista de tuplas (índice, score combinado, texto do documento)
        """
        try:
            if not isinstance(query, str) or not isinstance(documents, list):
                self.logger.error("Query deve ser string e documents deve ser lista de strings.")
                raise ValueError("Entradas inválidas.")
            if not documents:
                return []
            # Verificação de fallback
            if len(documents) == 0:
                return []
                
            # Pré-computa embeddings para todos os documentos
            doc_embeddings = np.array([self._get_embedding(doc) for doc in documents])
            
            # Executa ambos os retrievers
            sparse_results = self._sparse_retrieval(query, documents, k*2)  # Pega mais resultados para reranking
            dense_results = self._dense_retrieval(query, doc_embeddings, k*2)
            
            # Combina scores
            combined_scores = {}
            for idx, score in sparse_results:
                combined_scores[idx] = combined_scores.get(idx, 0) + score * self.sparse_weight
                
            for idx, score in dense_results:
                combined_scores[idx] = combined_scores.get(idx, 0) + score * self.dense_weight
                
            # Ordena por score combinado
            sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Pega os top-k
            top_results = sorted_results[:k]
            
            # Aplica reranking se solicitado
            if use_reranking and len(top_results) > 1:
                reranked_results = self._rerank(query, [documents[idx] for idx, _ in top_results])
                top_results = [(top_results[i][0], reranked_results[i][1], documents[top_results[i][0]]) 
                              for i in range(len(reranked_results))]
            else:
                top_results = [(idx, score, documents[idx]) for idx, score in top_results]
                
            return top_results
        except Exception as e:
            self.logger.error(f"Erro na recuperação híbrida: {str(e)}")
            # Fallback para BM25 em caso de erro
            return self._fallback_retrieval(query, documents, k)

    def _rerank(self, query: str, documents: List[str]) -> List[Tuple[int, float]]:
        """
        Aplica reranking usando cross-encoder.
        
        Args:
            query: Texto da consulta
            documents: Documentos para rerankear
            
        Returns:
            Lista de tuplas (índice original, novo score)
        """
        try:
            # Prepara pares query-doc
            pairs = [[query, doc] for doc in documents]
            
            # Prediz scores
            scores = self.reranker.predict(pairs)
            
            # Ordena por score
            ranked_indices = np.argsort(scores)[::-1]
            
            return [(i, scores[i]) for i in ranked_indices]
        except Exception as e:
            self.logger.error(f"Erro no reranking: {str(e)}")
            # Retorna ordem original em caso de erro
            return [(i, 0.0) for i in range(len(documents))]

    def _fallback_retrieval(self, query: str, documents: List[str], k: int) -> List[Tuple[int, float, str]]:
        """
        Método de fallback usando apenas BM25.
        
        Args:
            query: Texto da consulta
            documents: Documentos para buscar
            k: Número de resultados
            
        Returns:
            Lista de tuplas (índice, score, texto)
        """
        self.logger.warning("Usando fallback BM25 devido a erro no retriever principal")
        sparse_results = self._sparse_retrieval(query, documents, k)
        return [(idx, score, documents[idx]) for idx, score in sparse_results]