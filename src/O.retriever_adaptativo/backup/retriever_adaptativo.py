import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class RetrieverAdaptativo:
    def __init__(self, negative_mining_threshold: float = 0.5):
        """
        Inicializa o componente de Retriever Adaptativo.

        Args:
            negative_mining_threshold (float): Limiar de score/confiança abaixo do qual
                                               uma resposta é considerada um "hard negative" para mineração.
        """
        self.negative_mining_threshold = negative_mining_threshold
        logger.info(f"RetrieverAdaptativo inicializado com limiar de hard negative: {self.negative_mining_threshold}")

    def _identify_hard_negatives(self, evaluation_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifica exemplos de "hard negatives" com base nos resultados da avaliação.
        Hard negatives são consultas onde o sistema teve um desempenho ruim (e.g., baixa pontuação,
        avaliação negativa do LLM Judge, ou indicação de falta de contexto).
        """
        hard_negatives = []
        for item in evaluation_results:
            query = item.get("query", "")
            answer = item.get("answer", "")
            
            # Se a query ou answer estiverem faltando, não podemos avaliar.
            if not query or not answer:
                logger.debug(f"Skipping evaluation for item due to missing query or answer: {item}")
                continue

            is_hard_negative = False
            
            # Critério 1: Avaliação automática (se disponível e relevante)
            if "avaliacao_automatica" in item and "rouge" in item["avaliacao_automatica"]:
                rouge_l = item["avaliacao_automatica"]["rouge"].get("rougeL", 0.0)
                if rouge_l < self.negative_mining_threshold: # Usando o threshold para ROUGE-L
                    is_hard_negative = True
            
            # Critério 2: Avaliação do LLM Judge
            llm_judge_feedback = item.get("avaliacao_llm_judge", "").lower()
            if "genérica" in llm_judge_feedback or "não encontrou" in llm_judge_feedback or "ruim" in llm_judge_feedback:
                is_hard_negative = True
            
            # Critério 3: Resposta do LLM indica falha em encontrar informação
            if "não foi possível encontrar uma resposta" in answer.lower() or "não sei" in answer.lower():
                is_hard_negative = True

            if is_hard_negative:
                hard_negatives.append({
                    "query": query,
                    "answer": answer,
                    "context_documents": item.get("context_documents", []),
                    "evaluation": {
                        "automatic": item.get("avaliacao_automatica"),
                        "llm_judge": item.get("avaliacao_llm_judge")
                    }
                })
                logger.info(f"Identificado hard negative para a consulta: '{query}'")
        
        return hard_negatives

    def _trigger_fine_tuning(self, hard_negatives: List[Dict[str, Any]]):
        """
        (Simulado) Dispara o processo de fine-tuning progressivo do retriever.
        Em uma implementação real, isso envolveria:
        - Preparação de um dataset de treinamento a partir dos hard negatives.
        - Chamada a um serviço/função de fine-tuning para o modelo de embeddings ou retriever.
        - Monitoramento do processo de fine-tuning.
        """
        if hard_negatives:
            logger.warning(f"Processo de fine-tuning do retriever disparado com {len(hard_negatives)} hard negatives.")
            # Aqui, em um sistema real, você passaria os hard_negatives para um pipeline de fine-tuning.
            # Por exemplo, salvar em um banco de dados para um job de treinamento offline.
        else:
            logger.info("Nenhum hard negative identificado. Fine-tuning não disparado.")

    def run(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa a lógica do Retriever Adaptativo: identifica hard negatives e dispara fine-tuning.

        Args:
            evaluation_results (List[Dict[str, Any]]): Resultados da avaliação contínua.

        Returns:
            Dict[str, Any]: Um dicionário contendo os hard negatives identificados e um status.
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