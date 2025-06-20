from typing import List, Dict, Any, Optional
import numpy as np
import logging

class RerankingCrossEncoder:
    """
    Reranking com Cross-Encoder, combinando dense/sparse com pesos dinâmicos.
    Permite calibrar pesos via grid search.
    """

    def __init__(
        self,
        cross_encoder_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        dense_weight: float = 0.6,
        sparse_weight: float = 0.4,
        grid_search: bool = False,
        log_level: int = logging.INFO
    ):
        from sentence_transformers import CrossEncoder
        self.cross_encoder = CrossEncoder(cross_encoder_model)
        self.dense_weight = dense_weight
        self.sparse_weight = sparse_weight
        self.grid_search = grid_search
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("RerankingCrossEncoder")

    def calibrar_pesos(self, resultados: List[Dict[str, Any]], y_true: List[int], grid: Optional[List[float]] = None):
        """
        Calibra pesos dense/sparse via grid search para maximizar métrica (ex: MAP).
        """
        if not grid:
            grid = np.arange(0.0, 1.05, 0.05)
        melhor_score = -np.inf
        melhor_pesos = (self.dense_weight, self.sparse_weight)
        for dw in grid:
            sw = 1.0 - dw
            score = self._avaliar_pesos(resultados, y_true, dw, sw)
            if score > melhor_score:
                melhor_score = score
                melhor_pesos = (dw, sw)
        self.dense_weight, self.sparse_weight = melhor_pesos
        self.logger.info(f"Pesos calibrados: dense={self.dense_weight:.2f}, sparse={self.sparse_weight:.2f}")

    def _avaliar_pesos(self, resultados, y_true, dw, sw):
        # Stub: retorna score aleatório (implemente MAP real conforme necessidade)
        import random
        return random.uniform(0, 1)

    def combinar_scores(self, dense_score, sparse_score):
        return self.dense_weight * dense_score + self.sparse_weight * sparse_score
    
    def rerank(self, query: str, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recebe query e lista de docs (cada doc com 'dense_score', 'sparse_score', 'texto').
        Retorna docs reranqueados pelo Cross-Encoder e score combinado.
        """
        if not isinstance(query, str) or not isinstance(docs, list):
            self.logger.error("Query deve ser string e docs deve ser lista de dicts.")
            raise ValueError("Entradas inválidas.")
        pares = [[query, doc.get("texto", "")] for doc in docs]
        ce_scores = self.cross_encoder.predict(pares)
        for i, doc in enumerate(docs):
            doc["cross_score"] = float(ce_scores[i])
            doc["score_final"] = self.combinar_scores(
                doc.get("dense_score", 0), doc.get("sparse_score", 0)
            ) * 0.7 + doc["cross_score"] * 0.3
        docs_ordenados = sorted(docs, key=lambda d: d["score_final"], reverse=True)
        return docs_ordenados
    def run(self, resultados_retriever: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recebe lista de dicts com 'query' e 'resultados' (docs), retorna lista reranqueada.
        """
        reranked = []
        for item in resultados_retriever:
            query = item.get("query", "")
            docs = item.get("resultados", [])
            # Espera-se que cada doc tenha 'dense_score', 'sparse_score', 'texto'
            reranked_docs = self.rerank(query, docs)
            reranked.append({"query": query, "resultados": reranked_docs})
        return reranked