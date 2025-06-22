import logging
from typing import List, Dict, Any, Optional
import numpy as np

# Importações com tratamento de erro para facilitar o feedback ao usuário e a testabilidade.
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    util = None

logger = logging.getLogger(__name__)

class LLMcomRAGMerge:
    """
    Componente LLM com RAG que une as melhores práticas de design:
    - Injeção de dependência para alta testabilidade e flexibilidade.
    - Capacidade de carregar modelos padrão por nome para facilidade de uso.
    - Lógica robusta de seleção de exemplos (few-shot) e construção de prompts.
    """

    def __init__(self, 
                 llm_client: Any,
                 embedder: Optional[Any] = None,
                 embedder_model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
                 few_shot_examples: Optional[List[Dict[str, str]]] = None,
                 similarity_threshold: float = 0.65):
        """
        Inicializa o componente LLM com RAG.

        Args:
            llm_client (Any): Um cliente LLM funcional que possua um método `generate(prompt: str) -> str`.
            embedder (Any, optional): Uma instância de um modelo de embedding (ex: SentenceTransformer).
                                      Se None, tentará carregar um usando `embedder_model_name`.
            embedder_model_name (str): Nome do modelo de embedding a ser carregado se `embedder` não for fornecido.
            few_shot_examples (list, optional): Lista de exemplos few-shot. Cada dict deve ter chaves 'query' e 'answer'.
            similarity_threshold (float): Limiar de similaridade para a seleção dinâmica de exemplos.
        """
        if not hasattr(llm_client, 'generate') or not callable(llm_client.generate):
            raise TypeError("O `llm_client` deve ter um método `generate` que seja chamável.")

        self.llm_client = llm_client
        self.similarity_threshold = similarity_threshold
        self.few_shot_examples = few_shot_examples or self._get_default_few_shot_examples()
        
        self.embedder = embedder
        if not self.embedder:
            if SentenceTransformer:
                try:
                    self.embedder = SentenceTransformer(embedder_model_name)
                    logger.info(f"Embedder '{embedder_model_name}' carregado com sucesso.")
                except Exception as e:
                    logger.error(f"Falha ao carregar o modelo embedder '{embedder_model_name}': {e}")
            else:
                logger.warning("sentence-transformers não está instalado. A seleção dinâmica de exemplos será desativada.")

        self.few_shot_embeddings = None
        if self.embedder and self.few_shot_examples:
            try:
                example_queries = [ex['query'] for ex in self.few_shot_examples]
                self.few_shot_embeddings = self.embedder.encode(example_queries, convert_to_tensor=True)
            except Exception as e:
                logger.error(f"Erro ao gerar embeddings para os exemplos few-shot: {e}")

        logger.info("LLMcomRAGMerge inicializado.")

    def _get_default_few_shot_examples(self) -> List[Dict[str, str]]:
        """Fornece um conjunto padrão de exemplos genéricos."""
        return [
            {"query": "O que é IA?", "answer": "IA é a sigla para Inteligência Artificial."},
            {"query": "Qual a capital do Brasil?", "answer": "A capital do Brasil é Brasília."},
        ]

    def _selecionar_exemplos_few_shot(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        """Seleciona os exemplos few-shot mais similares à consulta usando `util.cos_sim`."""
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
        """Constrói o prompt final para o LLM de forma estruturada."""
        prompt_parts = ["Você é um assistente prestativo. Responda à pergunta do usuário com base no contexto fornecido.\n"]
        
        if few_shot_examples:
            prompt_parts.append("--- Exemplos de Perguntas e Respostas ---")
            for ex in few_shot_examples:
                prompt_parts.append(f"Pergunta: {ex['query']}\nResposta: {ex['answer']}\n")
        
        prompt_parts.append("--- Contexto Relevante ---")
        for i, doc in enumerate(context_docs):
            prompt_parts.append(f"Documento [{i+1}]: {doc}")
        
        prompt_parts.append("\n--- Pergunta do Usuário ---")
        prompt_parts.append(f"Pergunta: {query}")
        prompt_parts.append("\nResposta:")
        
        return "\n".join(prompt_parts)

    def run(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera uma resposta para uma única consulta usando o pipeline RAG."""
        if not query:
            raise ValueError("A consulta (query) não pode ser vazia.")

        selected_examples = self._selecionar_exemplos_few_shot(query)
        context_docs = [doc["document"] for doc in retrieved_docs]
        prompt = self._construir_prompt(query, context_docs, selected_examples)
        
        try:
            answer = self.llm_client.generate(prompt)
            return {"query": query, "answer": answer, "context_documents": context_docs, "prompt_used": prompt}
        except Exception as e:
            logger.error(f"Erro ao chamar LLM para a consulta '{query}': {e}")
            raise  # Re-lança a exceção para que a camada superior possa tratá-la.