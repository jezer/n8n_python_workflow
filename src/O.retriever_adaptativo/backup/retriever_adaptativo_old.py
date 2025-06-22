from typing import List, Dict, Any, Optional
import logging

class RetrieverAdaptativo:
    """
    Fine-tuning do retriever via active learning para hard negatives.
    Identifica falsos positivos, realiza fine-tuning progressivo e permite early stopping.
    """

    def __init__(
        self,
        retriever_model=None,  # Ex: SentenceTransformer, stub por padrão
        learning_rate: float = 2e-5,
        max_epochs: int = 3,
        early_stopping_rounds: int = 2,
        log_level: int = logging.INFO
    ):
        self.retriever_model = retriever_model or self._stub_model
        self.learning_rate = learning_rate
        self.max_epochs = max_epochs
        self.early_stopping_rounds = early_stopping_rounds
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("RetrieverAdaptativo")

    def _stub_model(self, *args, **kwargs):
        return "Modelo stub: fine-tuning não realizado."

    def identificar_hard_negatives(self, avaliacoes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifica falsos positivos (hard negatives) a partir das avaliações.
        """
        hard_negatives = []
        for item in avaliacoes:
            auto = item.get("avaliacao_automatica", {})
            # Exemplo: score baixo de ROUGE ou BERTScore indica hard negative
            if auto and (auto.get("rougeL", 1.0) < 0.3 or auto.get("bertscore_F1", 1.0) < 0.6):
                hard_negatives.append(item)
        self.logger.info(f"Hard negatives identificados: {len(hard_negatives)}")
        return hard_negatives

    def fine_tune(self, hard_negatives: List[Dict[str, Any]], positive_examples: Optional[List[Dict[str, Any]]] = None):
        """
        Realiza fine-tuning do retriever usando hard negatives e exemplos positivos.
        """
        self.logger.info("Fine-tuning iniciado (stub).")
        # Aqui entraria o código real de fine-tune, usando SentenceTransformer ou Trainer do HuggingFace.
        # Exemplo: montar pares (query, doc_negativo), (query, doc_positivo)
        # Implementar early stopping baseado em loss de validação.
        return "Fine-tuning realizado (stub)."
        
    def identificar_hard_negatives(self, avaliacoes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Orquestra identificação de hard negatives e fine-tuning do retriever.
        """
        hard_negatives = []
        for item in avaliacoes:
            auto = item.get("avaliacao_automatica", {})
            rouge = auto.get("rougeL")
            bert = auto.get("bertscore_F1")
            if (isinstance(rouge, (int, float)) and rouge < 0.3) or (isinstance(bert, (int, float)) and bert < 0.6):
                hard_negatives.append(item)
        self.logger.info(f"Hard negatives identificados: {len(hard_negatives)}")
        return hard_negatives