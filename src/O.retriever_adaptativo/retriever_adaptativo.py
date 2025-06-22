import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class RetrieverAdaptativoMerge:
    """
    Identifica "hard negatives" a partir de resultados de avaliação e dispara um
    processo de fine-tuning. Une a lógica de detecção sofisticada com o padrão
    de injeção de dependência para alta testabilidade e flexibilidade.
    """

    def __init__(self,
                 fine_tuning_client: Optional[Any] = None,
                 negative_mining_threshold: float = 0.5,
                 negative_judge_keywords: Optional[List[str]] = None,
                 negative_answer_keywords: Optional[List[str]] = None):
        """
        Inicializa o componente de Retriever Adaptativo.

        Args:
            fine_tuning_client (Any, optional): Um cliente ou função que lida com o processo
                                                de fine-tuning. Deve ter um método `trigger(hard_negatives)`.
            negative_mining_threshold (float): Limiar de score (ex: ROUGE-L) abaixo do qual
                                               uma resposta é considerada um "hard negative".
            negative_judge_keywords (List[str], optional): Palavras-chave no feedback do LLM Judge
                                                           que indicam uma resposta ruim.
            negative_answer_keywords (List[str], optional): Frases na resposta gerada que
                                                            indicam uma falha.
        """
        self.fine_tuning_client = fine_tuning_client
        self.negative_mining_threshold = negative_mining_threshold
        
        # Define palavras-chave padrão se nenhuma for fornecida
        self.negative_judge_keywords = negative_judge_keywords or ["genérica", "não encontrou", "ruim", "incorret"]
        self.negative_answer_keywords = negative_answer_keywords or ["não foi possível encontrar", "não sei", "desculpe, mas não"]

        logger.info(f"RetrieverAdaptativoMerge inicializado com limiar de {self.negative_mining_threshold}.")

    def _is_hard_negative(self, item: Dict[str, Any]) -> bool:
        """Verifica se um único item de avaliação é um "hard negative" com base em múltiplos critérios."""
        query = item.get("query", "")
        answer = item.get("answer", "")

        if not query or not answer:
            return False

        # Critério 1: Avaliação automática (score baixo)
        automatic_eval = item.get("avaliacao_automatica", {})
        if automatic_eval and "rouge" in automatic_eval:
            rouge_l = automatic_eval["rouge"].get("rougeL", 1.0)
            if isinstance(rouge_l, (float, int)) and rouge_l < self.negative_mining_threshold:
                return True

        # Critério 2: Avaliação do LLM Judge (feedback negativo)
        llm_judge_feedback = item.get("avaliacao_llm_judge", "").lower()
        if any(keyword in llm_judge_feedback for keyword in self.negative_judge_keywords):
            return True

        # Critério 3: Resposta do LLM indica falha
        if any(keyword in answer.lower() for keyword in self.negative_answer_keywords):
            return True

        return False

    def _identify_hard_negatives(self, evaluation_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filtra a lista de resultados de avaliação para encontrar todos os "hard negatives"."""
        hard_negatives = []
        for item in evaluation_results:
            if self._is_hard_negative(item):
                logger.info(f"Identificado hard negative para a consulta: '{item.get('query')}'")
                # Formata o dado para o processo de fine-tuning
                hard_negatives.append({
                    "query": item.get("query"),
                    "answer": item.get("answer"),
                    "context_documents": item.get("context_documents", []),
                    "evaluation": {
                        "automatic": item.get("avaliacao_automatica"),
                        "llm_judge": item.get("avaliacao_llm_judge")
                    }
                })
        return hard_negatives

    def _trigger_fine_tuning(self, hard_negatives: List[Dict[str, Any]]):
        """Dispara o processo de fine-tuning usando o cliente injetado."""
        if not hard_negatives:
            logger.info("Nenhum hard negative identificado. Fine-tuning não foi disparado.")
            return

        if self.fine_tuning_client and hasattr(self.fine_tuning_client, 'trigger'):
            try:
                self.fine_tuning_client.trigger(hard_negatives)
                logger.info(f"Cliente de fine-tuning disparado com {len(hard_negatives)} hard negatives.")
            except Exception as e:
                logger.error(f"Erro ao disparar o cliente de fine-tuning: {e}")
        else:
            logger.warning(f"Fine-tuning deveria ser disparado com {len(hard_negatives)} hard negatives, mas nenhum cliente funcional foi fornecido.")

    def run(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa a lógica do Retriever Adaptativo: identifica hard negatives e dispara fine-tuning.

        Args:
            evaluation_results (List[Dict[str, Any]]): Resultados da avaliação contínua.

        Returns:
            Um dicionário com o relatório da operação.
        """
        if not evaluation_results:
            logger.info("Nenhum resultado de avaliação fornecido. Nenhuma adaptação será realizada.")
            return {"status": "no_evaluation_results", "hard_negatives_identified": []}

        hard_negatives = self._identify_hard_negatives(evaluation_results)
        self._trigger_fine_tuning(hard_negatives)

        return {
            "status": "adaptation_process_completed",
            "hard_negatives_identified": hard_negatives,
            "num_hard_negatives": len(hard_negatives)
        }