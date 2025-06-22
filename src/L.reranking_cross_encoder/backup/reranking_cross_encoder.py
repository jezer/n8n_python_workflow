import logging
from typing import List, Dict, Any
from sentence_transformers import CrossEncoder # Assuming this is the intended CrossEncoder

logger = logging.getLogger(__name__)

class RerankingCrossEncoder:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.reranker = None
        try:
            self.reranker = CrossEncoder(model_name)
            logger.info(f"Cross-encoder model '{model_name}' loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load cross-encoder model '{model_name}': {e}")
            self.reranker = None # Ensure it's None if loading fails

    def run(self, retrieval_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Reranks retrieved documents for each query using a cross-encoder.

        Args:
            retrieval_results: A list of dictionaries, where each dictionary
                               contains "query" (str) and "resultados" (List[Dict[str, Any]]).
                               Each item in "resultados" should have "document" (str) and "score" (float).

        Returns:
            A list of dictionaries with the same structure as input, but with
            "resultados" reranked and updated scores.
        """
        if not self.reranker:
            logger.warning("Reranker model not loaded. Skipping reranking step.")
            return retrieval_results # Return original results if model not loaded

        reranked_output = []
        for item in retrieval_results:
            query = item.get("query")
            retrieved_docs = item.get("resultados", [])

            if not query or not retrieved_docs:
                reranked_output.append(item) # Append original if no query or no docs
                continue

            # Prepare pairs for cross-encoder
            # Each pair is [query, document_text]
            pairs = [[query, doc["document"]] for doc in retrieved_docs]

            try:
                # Predict scores using the cross-encoder
                # The output scores are typically similarity scores
                cross_encoder_scores = self.reranker.predict(pairs)

                # Combine original retrieved docs with new cross-encoder scores
                # and sort them by the new score
                reranked_docs = []
                for i, doc in enumerate(retrieved_docs):
                    reranked_docs.append({
                        "document": doc["document"],
                        "score": float(cross_encoder_scores[i]), # Use cross-encoder score
                        "original_score": doc["score"], # Keep original score for reference
                        "idx": doc.get("idx") # Preserve original index if present
                    })
                
                # Sort by the new cross-encoder score in descending order
                reranked_docs.sort(key=lambda x: x["score"], reverse=True)

                reranked_output.append({
                    "query": query,
                    "resultados": reranked_docs
                })

            except Exception as e:
                logger.error(f"Error during reranking for query '{query}': {e}. Returning original results for this query.")
                reranked_output.append(item) # Return original results for this query on error

        return reranked_output