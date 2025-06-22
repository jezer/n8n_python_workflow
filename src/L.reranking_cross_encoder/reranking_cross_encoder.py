import logging
from typing import List, Dict, Any
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

class RerankerCombinado:
    """
    Reranking com Cross-Encoder que combina o score inicial do retriever com o score
    do cross-encoder através de uma ponderação configurável, unindo as melhores
    práticas de robustez e lógica de combinação.
    """

    def __init__(self, 
                 model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
                 cross_encoder_weight: float = 0.5):
        """
        Inicializa o Reranker.

        Args:
            model_name (str): O nome do modelo CrossEncoder a ser carregado.
            cross_encoder_weight (float): O peso a ser dado ao score do cross-encoder (entre 0 e 1).
                                          O score do retriever inicial terá o peso (1 - cross_encoder_weight).
        """
        if not 0.0 <= cross_encoder_weight <= 1.0:
            raise ValueError("cross_encoder_weight deve estar entre 0.0 e 1.0")

        self.model_name = model_name
        self.cross_encoder_weight = cross_encoder_weight
        self.retriever_weight = 1.0 - cross_encoder_weight
        self.reranker = None

        try:
            self.reranker = CrossEncoder(model_name)
            logger.info(f"Cross-encoder model '{model_name}' loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load cross-encoder model '{model_name}': {e}")
            # self.reranker permanece None, o que será tratado no método run.

    def run(self, retrieval_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Reranqueia documentos combinando o score do retriever com o do cross-encoder.

        Args:
            retrieval_results: Uma lista de dicionários, onde cada um contém "query" e "resultados".
                               Cada item em "resultados" deve ter "document" (str) e "score" (float).

        Returns:
            A lista de resultados com os documentos reranqueados e um "final_score" combinado.
        """
        if not self.reranker:
            logger.warning("Reranker model not loaded. Skipping reranking step and returning original results.")
            return retrieval_results

        reranked_output = []
        for item in retrieval_results:
            query = item.get("query")
            retrieved_docs = item.get("resultados", [])

            if not query or not retrieved_docs:
                reranked_output.append(item)
                continue

            pairs = [[query, doc["document"]] for doc in retrieved_docs]

            try:
                cross_encoder_scores = self.reranker.predict(pairs)

                reranked_docs = []
                for i, doc in enumerate(retrieved_docs):
                    initial_score = doc.get("score", 0.0)
                    cross_score = float(cross_encoder_scores[i])

                    # Combinação ponderada dos scores
                    final_score = (initial_score * self.retriever_weight) + (cross_score * self.cross_encoder_weight)

                    doc_result = doc.copy() # Evita modificar o dicionário original
                    doc_result["score"] = final_score # Atualiza o score principal
                    doc_result["original_retriever_score"] = initial_score
                    doc_result["cross_encoder_score"] = cross_score
                    reranked_docs.append(doc_result)
                
                reranked_docs.sort(key=lambda x: x["score"], reverse=True)
                reranked_output.append({"query": query, "resultados": reranked_docs})

            except Exception as e:
                logger.error(f"Error during reranking for query '{query}': {e}. Returning original results for this query.")
                reranked_output.append(item)

        return reranked_output

