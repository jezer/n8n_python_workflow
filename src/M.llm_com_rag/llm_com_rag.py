from typing import List, Dict, Any, Optional
import numpy as np
import logging

class LLMcomRAG:
    """
    LLM com RAG: few-shot prompting dinâmico por tópico.
    Seleciona top-3 exemplos mais similares à query via embeddings.
    Fallback para exemplos genéricos se similaridade < 0.65.
    """

    def __init__(
        self,
        llm_client=None,  # Deve ter método generate(prompt) -> resposta
        exemplos_few_shot: Optional[List[Dict[str, str]]] = None,
        embedding_model=None,
        similarity_threshold: float = 0.65,
        log_level: int = logging.INFO
    ):
        from sentence_transformers import SentenceTransformer
        self.llm_client = llm_client or self._stub_llm
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model or SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.exemplos_few_shot = exemplos_few_shot or [
            {"pergunta": "O que é Python?", "resposta": "Python é uma linguagem de programação."},
            {"pergunta": "Para que serve o FAISS?", "resposta": "FAISS é usado para busca vetorial eficiente."},
            {"pergunta": "O que é RAG?", "resposta": "RAG é Retrieval-Augmented Generation."}
        ]
        self.embeddings_few_shot = self.embedding_model.encode(
            [ex["pergunta"] for ex in self.exemplos_few_shot]
        )
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("LLMcomRAG")

    def _stub_llm(self, prompt: str) -> str:
        return "Resposta gerada automaticamente (stub)."

    def _similaridade(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        emb1 = emb1 / (np.linalg.norm(emb1) + 1e-8)
        emb2 = emb2 / (np.linalg.norm(emb2) + 1e-8)
        return float(np.dot(emb1, emb2))

    def selecionar_few_shots(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        query_emb = self.embedding_model.encode([query])[0]
        sims = [self._similaridade(query_emb, emb) for emb in self.embeddings_few_shot]
        top_indices = np.argsort(sims)[::-1][:top_k]
        selecionados = [self.exemplos_few_shot[i] for i in top_indices if sims[i] >= self.similarity_threshold]
        if not selecionados:
            self.logger.info("Similaridade baixa, usando exemplos genéricos.")
            return self.exemplos_few_shot[:top_k]
        return selecionados

    def montar_prompt(self, query: str, contexto: str, few_shots: List[Dict[str, str]]) -> str:
        exemplos = "\n".join([f"Q: {ex['pergunta']}\nA: {ex['resposta']}" for ex in few_shots])
        prompt = (
            f"{exemplos}\n\nContexto:\n{contexto}\n\nQ: {query}\nA:"
        )
        return prompt

    def run(self, resultados_reranking: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recebe lista 
        de dicts com 'query', 'resultados' (docs relevantes), gera resposta do LLM com few-shot dinâmico.
        """
        respostas = []
        for item in resultados_reranking:
            query = item.get("query", "")
            docs = item.get("resultados", [])
            if not query or not isinstance(docs, list):
                self.logger.warning("Item malformado: %s", item)
                continue
            contexto = "\n".join([doc[2] if isinstance(doc, (list, tuple)) and len(doc) > 2 else str(doc) for doc in docs])
            few_shots = self.selecionar_few_shots(query)
            prompt = self.montar_prompt(query, contexto, few_shots)
            try:
                resposta = self.llm_client(prompt)
            except Exception as e:
                self.logger.error(f"Erro ao chamar LLM: {e}")
                resposta = "Erro ao gerar resposta."
            respostas.append({
                "query": query,
                "resposta": resposta,
                "prompt": prompt,
                "few_shots_utilizados": few_shots
            })
            self.logger.info(f"Resposta gerada para query: {query}")
        return respostas