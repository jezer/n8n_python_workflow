import logging
from typing import List, Dict, Any, Optional
import numpy as np

# Importações com tratamento de erro para facilitar o feedback ao usuário
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    util = None

logger = logging.getLogger(__name__)

class LLMcomRAG:
    def __init__(self, 
                 llm_model_name: str = "gpt-4", 
                 embedder_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
                 few_shot_examples: Optional[List[Dict[str, str]]] = None,
                 similarity_threshold: float = 0.65):
        """
        Inicializa o componente LLM com RAG.

        Args:
            llm_model_name (str): Identificador do LLM a ser utilizado.
            embedder_model_name (str): Modelo para embedding dos exemplos few-shot.
            few_shot_examples (list, optional): Lista de exemplos few-shot.
            similarity_threshold (float): Limiar para a seleção dinâmica de exemplos.
        """
        self.llm_model_name = llm_model_name
        self.similarity_threshold = similarity_threshold
        self.few_shot_examples = few_shot_examples or self._get_default_few_shot_examples()
        
        self.embedder = None
        self.few_shot_embeddings = None
        if SentenceTransformer:
            try:
                self.embedder = SentenceTransformer(embedder_model_name)
                if self.few_shot_examples:
                    example_queries = [ex['query'] for ex in self.few_shot_examples]
                    self.few_shot_embeddings = self.embedder.encode(example_queries, convert_to_tensor=True)
                logger.info(f"Embedder '{embedder_model_name}' carregado para seleção few-shot.")
            except Exception as e:
                logger.error(f"Falha ao carregar o modelo embedder '{embedder_model_name}': {e}")
        else:
            logger.warning("sentence-transformers não está instalado. A seleção dinâmica de exemplos será desativada.")

        logger.info(f"LLMcomRAG inicializado para o modelo '{self.llm_model_name}'.")

    def _get_default_few_shot_examples(self) -> List[Dict[str, str]]:
        """Fornece um conjunto padrão de exemplos genéricos."""
        return [
            {"query": "O que é IA?", "answer": "IA é a sigla para Inteligência Artificial."},
            {"query": "Qual a capital do Brasil?", "answer": "A capital do Brasil é Brasília."},
        ]

    def _selecionar_exemplos_few_shot(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """Seleciona os exemplos few-shot mais similares à consulta."""
        if not self.embedder or self.few_shot_embeddings is None or not self.few_shot_examples:
            return []

        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        similarities = util.cos_sim(query_embedding, self.few_shot_embeddings)[0]
        top_k_indices = np.argsort(-similarities)[:k]

        selected_examples = [self.few_shot_examples[idx] for idx in top_k_indices if similarities[idx] >= self.similarity_threshold]
        
        if not selected_examples:
            logger.info(f"Similaridade abaixo do limiar {self.similarity_threshold}. Usando exemplos genéricos de fallback.")
            return self.few_shot_examples[:k]
            
        return selected_examples

    def _construir_prompt(self, query: str, context_docs: List[str], few_shot_examples: List[Dict[str, str]]) -> str:
        """Constrói o prompt final para o LLM."""
        prompt_parts = ["Você é um assistente prestativo. Responda à pergunta do usuário com base no contexto fornecido.\n"]
        
        if few_shot_examples:
            prompt_parts.append("--- Exemplos ---")
            for ex in few_shot_examples:
                prompt_parts.append(f"Pergunta: {ex['query']}\nResposta: {ex['answer']}\n")
        
        prompt_parts.append("--- Contexto ---")
        for i, doc in enumerate(context_docs):
            prompt_parts.append(f"Documento [{i+1}]: {doc}")
        
        prompt_parts.append("\n--- Pergunta do Usuário ---")
        prompt_parts.append(f"Pergunta: {query}")
        prompt_parts.append("Resposta:")
        
        return "\n".join(prompt_parts)

    def _chamar_llm(self, prompt: str) -> str:
        """(Simulado) Realiza uma chamada ao LLM com o prompt fornecido."""
        logger.info(f"Chamando LLM com prompt de {len(prompt)} caracteres.")
        if "inteligência artificial" in prompt:
            return "Com base no Documento [1], inteligência artificial é um campo da ciência da computação."
        if "redes neurais" in prompt:
            return "Redes neurais são um subcampo do aprendizado de máquina, conforme mencionado no Documento [1]."
        return "Não foi possível encontrar uma resposta no contexto fornecido."

    def run(self, resultados_reranking: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gera respostas para uma lista de consultas usando o pipeline RAG."""
        final_results = []
        for item in resultados_reranking:
            query = item.get("query")
            reranked_docs = item.get("resultados", [])

            if not query: continue

            selected_examples = self._selecionar_exemplos_few_shot(query)
            context_docs = [doc["document"] for doc in reranked_docs]
            prompt = self._construir_prompt(query, context_docs, selected_examples)
            
            try:
                answer = self._chamar_llm(prompt)
                final_results.append({"query": query, "answer": answer, "context_documents": context_docs, "prompt_used": prompt})
            except Exception as e:
                logger.error(f"Erro ao chamar LLM para a consulta '{query}': {e}")
                final_results.append({"query": query, "answer": f"Erro ao gerar resposta: {e}", "context_documents": context_docs, "prompt_used": prompt})

        return final_results