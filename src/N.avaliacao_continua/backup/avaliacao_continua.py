import logging
from typing import List, Dict, Any, Optional

# Importações opcionais para feedback mais claro
try:
    import evaluate
    from evaluate import load as evaluate_load
except ImportError:
    evaluate = None
    evaluate_load = None

logger = logging.getLogger(__name__)

class AvaliacaoContinua:
    def __init__(self, llm_judge_model_name: str = "gpt-4"):
        """
        Inicializa o componente de Avaliação Contínua.

        Args:
            llm_judge_model_name (str): Nome do modelo LLM a ser usado como juiz.
        """
        self.llm_judge_model_name = llm_judge_model_name
        self.metrics = {}
        self._load_metrics()
        logger.info(f"AvaliacaoContinua inicializada. LLM Judge: {self.llm_judge_model_name}")

    def _load_metrics(self):
        """Carrega as métricas de avaliação automática."""
        if not evaluate:
            logger.warning("A biblioteca 'evaluate' não está instalada. Métricas automáticas desativadas.")
            return

        try:
            self.metrics['rouge'] = evaluate_load("rouge")
            logger.info("Métrica ROUGE carregada.")
        except Exception as e:
            logger.error(f"Falha ao carregar métrica ROUGE: {e}")

        try:
            self.metrics['bertscore'] = evaluate_load("bertscore")
            logger.info("Métrica BERTScore carregada.")
        except Exception as e:
            logger.error(f"Falha ao carregar métrica BERTScore: {e}")

        # Adicionar outras métricas conforme necessário (ex: citation precision)

    def _evaluate_automatic(self, predictions: List[str], references: List[str]) -> Dict[str, Any]:
        """Calcula métricas de avaliação automática."""
        results = {}
        if not predictions or not references:
            logger.warning("Previsões ou referências vazias para avaliação automática.")
            return results

        if 'rouge' in self.metrics:
            try:
                rouge_results = self.metrics['rouge'].compute(predictions=predictions, references=references)
                results['rouge'] = rouge_results
            except Exception as e:
                logger.error(f"Erro ao calcular ROUGE: {e}")

        if 'bertscore' in self.metrics:
            try:
                # BERTScore pode ser lento, considerar amostragem ou cache em produção
                bertscore_results = self.metrics['bertscore'].compute(predictions=predictions, references=references, lang="pt")
                results['bertscore'] = {
                    "precision": sum(bertscore_results['precision']) / len(bertscore_results['precision']),
                    "recall": sum(bertscore_results['recall']) / len(bertscore_results['recall']),
                    "f1": sum(bertscore_results['f1']) / len(bertscore_results['f1']),
                }
            except Exception as e:
                logger.error(f"Erro ao calcular BERTScore: {e}")
        
        return results

    def _evaluate_llm_as_judge(self, query: str, answer: str, context: List[str]) -> str:
        """
        (Simulado) Avalia a resposta usando um LLM como juiz.
        Em uma implementação real, isso envolveria uma chamada à API do LLM.
        """
        logger.info(f"Chamando LLM como juiz para a consulta: '{query}'")
        # Exemplo de lógica simulada
        if "inteligência artificial" in query and "campo da ciência da computação" in answer:
            return "Excelente resposta, concisa e precisa."
        elif "redes neurais" in query and "subcampo do aprendizado de máquina" in answer:
            return "Boa resposta, relevante ao contexto."
        elif "Não foi possível encontrar uma resposta" in answer:
            return "Resposta genérica, indica falta de informação no contexto."
        return "Avaliação padrão do LLM Judge."

    def run(self, resultados_llmrag: List[Dict[str, Any]], referencias: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Realiza a avaliação contínua das respostas do LLM.

        Args:
            resultados_llmrag (List[Dict[str, Any]]): Saída da etapa LLM com RAG.
                Cada item deve conter 'query', 'answer', 'context_documents'.
            referencias (Optional[List[Dict[str, Any]]]): Respostas de referência (ground truth).
                Cada item deve conter 'query' e 'answer'.

        Returns:
            List[Dict[str, Any]]: Resultados do LLM com RAG enriquecidos com avaliações.
        """
        evaluated_results = []
        for i, item in enumerate(resultados_llmrag):
            query = item.get("query", "")
            answer = item.get("answer", "")
            context = item.get("context_documents", [])
            
            current_references = [ref["answer"] for ref in referencias if ref["query"] == query] if referencias else []

            item["avaliacao_automatica"] = self._evaluate_automatic(predictions=[answer], references=current_references)
            item["avaliacao_llm_judge"] = self._evaluate_llm_as_judge(query, answer, context)
            
            evaluated_results.append(item)
        return evaluated_results