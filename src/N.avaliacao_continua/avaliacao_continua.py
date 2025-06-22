import logging
from typing import List, Dict, Any, Optional

# Importações opcionais para feedback mais claro e para permitir o carregamento padrão.
try:
    import evaluate
    from evaluate import load as evaluate_load
except ImportError:
    evaluate = None
    evaluate_load = None

logger = logging.getLogger(__name__)

class AvaliacaoContinuaMerge:
    """
    Componente de Avaliação Contínua que une as melhores práticas de design:
    - Suporte para injeção de dependência para alta testabilidade.
    - Carregamento padrão de métricas para facilidade de uso.
    - Processamento em lote (batch) para máxima eficiência.
    - Lógica robusta de tratamento de erros e correspondência de dados.
    """

    def __init__(self, 
                 llm_judge_client: Optional[Any] = None,
                 rouge_metric: Optional[Any] = None,
                 bertscore_metric: Optional[Any] = None):
        """
        Inicializa o componente de Avaliação Contínua.

        Args:
            llm_judge_client (Any, optional): Um cliente LLM funcional para avaliação.
            rouge_metric (Any, optional): Uma instância de uma métrica ROUGE.
            bertscore_metric (Any, optional): Uma instância de uma métrica BERTScore.
        """
        self.llm_judge_client = llm_judge_client or self._get_default_llm_judge()
        self.metrics = {}
        
        # Usa métricas injetadas ou tenta carregar as padrões.
        self.metrics['rouge'] = rouge_metric
        self.metrics['bertscore'] = bertscore_metric
        self._load_missing_metrics()

        logger.info("AvaliacaoContinuaMerge inicializada.")

    def _load_missing_metrics(self):
        """Carrega métricas padrão se não foram injetadas."""
        if not evaluate:
            logger.warning("A biblioteca 'evaluate' não está instalada. Métricas automáticas desativadas.")
            return

        if not self.metrics.get('rouge'):
            try:
                self.metrics['rouge'] = evaluate_load("rouge")
                logger.info("Métrica ROUGE padrão carregada.")
            except Exception as e:
                logger.error(f"Falha ao carregar métrica ROUGE padrão: {e}")

        if not self.metrics.get('bertscore'):
            try:
                self.metrics['bertscore'] = evaluate_load("bertscore")
                logger.info("Métrica BERTScore padrão carregada.")
            except Exception as e:
                logger.error(f"Falha ao carregar métrica BERTScore padrão: {e}")

    def _get_default_llm_judge(self) -> Any:
        """Retorna um cliente LLM Judge simulado padrão."""
        # Em uma implementação real, isso poderia carregar um cliente OpenAI, etc.
        mock_judge = lambda query, answer, context: "Avaliação padrão do LLM Judge."
        return mock_judge

    def _evaluate_automatic_batch(self, predictions: List[str], references: List[str]) -> List[Dict[str, Any]]:
        """Calcula métricas automáticas para um lote de previsões e referências."""
        batch_size = len(predictions)
        results_by_item = [{} for _ in range(batch_size)]

        if 'rouge' in self.metrics and self.metrics['rouge']:
            try:
                rouge_scores = self.metrics['rouge'].compute(predictions=predictions, references=references, use_aggregator=False)
                for i in range(batch_size):
                    results_by_item[i]['rouge'] = rouge_scores[i]
            except Exception as e:
                logger.error(f"Erro ao calcular ROUGE em lote: {e}")

        if 'bertscore' in self.metrics and self.metrics['bertscore']:
            try:
                bert_scores = self.metrics['bertscore'].compute(predictions=predictions, references=references, lang="pt")
                for i in range(batch_size):
                    results_by_item[i]['bertscore'] = {
                        "precision": bert_scores['precision'][i],
                        "recall": bert_scores['recall'][i],
                        "f1": bert_scores['f1'][i],
                    }
            except Exception as e:
                logger.error(f"Erro ao calcular BERTScore em lote: {e}")
        
        return results_by_item

    def run(self, resultados_llmrag: List[Dict[str, Any]], referencias: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Realiza a avaliação contínua das respostas do LLM de forma eficiente em lote.
        """
        if not resultados_llmrag:
            return []

        # Prepara dados para avaliação em lote
        predictions = [item.get("answer", "") for item in resultados_llmrag]
        queries = [item.get("query", "") for item in resultados_llmrag]
        
        # Mapeia referências por query para correspondência robusta
        mapa_referencias = {ref['query']: ref['answer'] for ref in referencias} if referencias else {}
        references_for_batch = [mapa_referencias.get(q, "") for q in queries]

        # 1. Avaliação Automática em Lote
        automatic_evals = []
        if any(references_for_batch): # Só executa se houver alguma referência
            automatic_evals = self._evaluate_automatic_batch(predictions, references_for_batch)
        else:
            automatic_evals = [{} for _ in resultados_llmrag]

        # 2. Avaliação com LLM Judge (em loop, pois geralmente é por item) e montagem final
        evaluated_results = []
        for i, item in enumerate(resultados_llmrag):
            enriched_item = item.copy()
            
            # Adiciona avaliação automática
            enriched_item["avaliacao_automatica"] = automatic_evals[i]
            
            # Adiciona avaliação do LLM Judge
            enriched_item["avaliacao_llm_judge"] = self.llm_judge_client(
                query=item.get("query", ""),
                answer=item.get("answer", ""),
                context=item.get("context_documents", [])
            )
            evaluated_results.append(enriched_item)
            
        return evaluated_results