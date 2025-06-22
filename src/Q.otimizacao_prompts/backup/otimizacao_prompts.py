import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class OtimizacaoPrompts:
    def __init__(self, llm_client=None):
        """
        Inicializa o componente de Otimização de Prompts.

        Args:
            llm_client: Um cliente LLM simulado ou real para gerar respostas.
                        Se não for fornecido, um cliente simulado padrão será usado.
        """
        # Em um cenário real, isso seria um cliente para OpenAI, Anthropic, etc.
        self.llm_client = llm_client
        logger.info("OtimizacaoPrompts inicializado.")

    def _construir_prompt(self, template: str, query: str, context: List[str]) -> str:
        """Constrói um prompt a partir de um template, consulta e contexto."""
        context_str = "\n".join([f"Documento {i+1}: {doc}" for i, doc in enumerate(context)])
        return template.format(context=context_str, query=query)

    def _avaliar_resposta(self, prediction: str, reference: str) -> Dict[str, float]:
        """
        (Simulado) Avalia uma resposta gerada contra uma referência.
        Em um sistema real, isso chamaria o módulo de avaliação (N)
        ou usaria métricas como ROUGE, BERTScore.
        Esta simulação simples favorece respostas mais longas e detalhadas.
        """
        score = len(prediction) / (len(reference) + 1e-5) if reference else 0
        return {"simulated_score": min(score, 1.5)} # Permite scores > 1 para mostrar diferença

    def _run_ab_test(self, evaluation_results: List[Dict[str, Any]], prompt_a: str, prompt_b: str, referencias: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executa um teste A/B entre dois templates de prompt."""
        if not self.llm_client:
            raise RuntimeError("Cliente LLM não foi configurado para o teste A/B.")

        resultados_a = []
        resultados_b = []
        
        # Mapeia query para resposta de referência para fácil acesso
        mapa_referencias = {ref['query']: ref['answer'] for ref in referencias}

        for item in evaluation_results:
            query = item.get("query")
            context = item.get("context_documents", [])
            
            if not query or query not in mapa_referencias:
                continue

            # Gerar e avaliar para Prompt A
            prompt_completo_a = self._construir_prompt(prompt_a, query, context)
            resposta_a = self.llm_client.generate(prompt_completo_a)
            avaliacao_a = self._avaliar_resposta(resposta_a, mapa_referencias[query])
            resultados_a.append(avaliacao_a['simulated_score'])

            # Gerar e avaliar para Prompt B
            prompt_completo_b = self._construir_prompt(prompt_b, query, context)
            resposta_b = self.llm_client.generate(prompt_completo_b)
            avaliacao_b = self._avaliar_resposta(resposta_b, mapa_referencias[query])
            resultados_b.append(avaliacao_b['simulated_score'])

        score_medio_a = sum(resultados_a) / len(resultados_a) if resultados_a else 0
        score_medio_b = sum(resultados_b) / len(resultados_b) if resultados_b else 0

        vencedor = "Prompt A" if score_medio_a >= score_medio_b else "Prompt B"

        return {
            "method": "a/b_test",
            "prompt_a_avg_score": score_medio_a,
            "prompt_b_avg_score": score_medio_b,
            "winner": vencedor,
            "num_samples_tested": len(resultados_a)
        }

    def run(self, evaluation_results: List[Dict[str, Any]], metodo: str = "ab_test", **kwargs) -> Dict[str, Any]:
        """
        Executa o processo de otimização de prompts.

        Args:
            evaluation_results: Resultados da avaliação contínua.
            metodo (str): O método de otimização a ser usado ('ab_test', 'star', etc.).
            **kwargs: Argumentos adicionais para o método específico.

        Returns:
            Um dicionário com o relatório da otimização.
        """
        if metodo == "ab_test":
            prompt_a = kwargs.get("prompt_a", "Contexto:\n{context}\n\nPergunta: {query}\nPrompt A: Resposta concisa:")
            prompt_b = kwargs.get("prompt_b", "Contexto fornecido:\n{context}\n\nSua tarefa é responder à seguinte pergunta do usuário com base estritamente nas informações do contexto.\nPergunta do usuário: {query}\nPrompt B: Resposta detalhada:")
            referencias = kwargs.get("referencias", [])
            
            if not referencias:
                logger.error("Referências (ground truth) são necessárias para o teste A/B.")
                return {"status": "error", "message": "Referências não fornecidas."}

            return self._run_ab_test(evaluation_results, prompt_a, prompt_b, referencias)
        
        # Adicionar outros métodos como 'star' aqui
        else:
            logger.warning(f"Método de otimização '{metodo}' não implementado.")
            return {"status": "unimplemented_method", "method": metodo}