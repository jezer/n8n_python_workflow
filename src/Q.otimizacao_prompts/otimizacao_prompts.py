import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class OtimizacaoPromptsMerge:
    """
    Componente para otimização de prompts que une as melhores práticas de design:
    - Injeção de dependência para o cliente LLM e o cliente de avaliação.
    - Lógica de teste A/B que utiliza corretamente o contexto do RAG.
    - Estrutura extensível para futuros métodos de otimização (ex: STaR).
    """

    def __init__(self, llm_client: Any, evaluation_client: Any):
        """
        Inicializa o componente de Otimização de Prompts.

        Args:
            llm_client (Any): Um cliente LLM funcional que possua um método `generate(prompt: str) -> str`.
            evaluation_client (Any): Um cliente de avaliação que possua um método para avaliar
                                     respostas (ex: `run(resultados, referencias)`).
        """
        if not hasattr(llm_client, 'generate') or not callable(llm_client.generate):
            raise TypeError("O `llm_client` deve ter um método `generate` que seja chamável.")
        if not hasattr(evaluation_client, 'run') or not callable(evaluation_client.run):
            raise TypeError("O `evaluation_client` deve ter um método `run` que seja chamável.")

        self.llm_client = llm_client
        self.evaluation_client = evaluation_client
        logger.info("OtimizacaoPromptsMerge inicializado.")

    def _construir_prompt(self, template: str, query: str, context: List[str]) -> str:
        """Constrói um prompt a partir de um template, consulta e contexto."""
        context_str = "\n".join([f"Documento {i+1}: {doc}" for i, doc in enumerate(context)])
        return template.format(context=context_str, query=query)

    def _run_ab_test(self, evaluation_dataset: List[Dict[str, Any]], prompt_a: str, prompt_b: str, referencias: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executa um teste A/B entre dois templates de prompt, utilizando um cliente de avaliação real.
        """
        logger.info("Iniciando teste A/B para os prompts.")
        
        # Gerar respostas para o Prompt A
        respostas_a = []
        for item in evaluation_dataset:
            query = item.get("query")
            context = item.get("context_documents", [])
            prompt_completo_a = self._construir_prompt(prompt_a, query, context)
            resposta_a = self.llm_client.generate(prompt_completo_a)
            respostas_a.append({"query": query, "answer": resposta_a, "context_documents": context})

        # Gerar respostas para o Prompt B
        respostas_b = []
        for item in evaluation_dataset:
            query = item.get("query")
            context = item.get("context_documents", [])
            prompt_completo_b = self._construir_prompt(prompt_b, query, context)
            resposta_b = self.llm_client.generate(prompt_completo_b)
            respostas_b.append({"query": query, "answer": resposta_b, "context_documents": context})

        # Avaliar os dois conjuntos de respostas
        avaliacoes_a = self.evaluation_client.run(respostas_a, referencias)
        avaliacoes_b = self.evaluation_client.run(respostas_b, referencias)

        # Calcular scores médios (exemplo usando ROUGE-L)
        score_medio_a = sum(
            res.get("avaliacao_automatica", {}).get("rouge", {}).get("rougeL", 0.0)
            for res in avaliacoes_a
        ) / len(avaliacoes_a) if avaliacoes_a else 0

        score_medio_b = sum(
            res.get("avaliacao_automatica", {}).get("rouge", {}).get("rougeL", 0.0)
            for res in avaliacoes_b
        ) / len(avaliacoes_b) if avaliacoes_b else 0

        vencedor = "Prompt A" if score_medio_a >= score_medio_b else "Prompt B"
        logger.info(f"Resultado do teste A/B: Vencedor = {vencedor} (A: {score_medio_a:.4f}, B: {score_medio_b:.4f})")

        return {
            "method": "a/b_test",
            "prompt_a_avg_score": score_medio_a,
            "prompt_b_avg_score": score_medio_b,
            "winner": vencedor,
            "num_samples_tested": len(evaluation_dataset)
        }

    def _run_star(self, evaluation_dataset: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """(Placeholder) Implementação futura da otimização STaR."""
        logger.warning("O método de otimização 'star' ainda não foi implementado.")
        return {"status": "unimplemented_method", "method": "star"}

    def run(self, evaluation_dataset: List[Dict[str, Any]], metodo: str = "ab_test", **kwargs) -> Dict[str, Any]:
        """
        Executa o processo de otimização de prompts.

        Args:
            evaluation_dataset: Um conjunto de dados de avaliação, contendo 'query' e 'context_documents'.
            metodo (str): O método de otimização a ser usado ('ab_test', 'star').
            **kwargs: Argumentos adicionais para o método específico.
                      Para 'ab_test', espera-se 'prompt_a', 'prompt_b', e 'referencias'.

        Returns:
            Um dicionário com o relatório da otimização.
        """
        if metodo == "ab_test":
            prompt_a = kwargs.get("prompt_a", "Contexto:\n{context}\n\nPergunta: {query}\nResposta concisa:")
            prompt_b = kwargs.get("prompt_b", "Com base no contexto fornecido:\n{context}\n\nResponda à seguinte pergunta:\n{query}\nResposta detalhada:")
            referencias = kwargs.get("referencias")
            
            if not referencias:
                logger.error("Referências (ground truth) são necessárias para o teste A/B.")
                return {"status": "error", "message": "Referências não fornecidas."}

            return self._run_ab_test(evaluation_dataset, prompt_a, prompt_b, referencias)
        
        elif metodo == "star":
            return self._run_star(evaluation_dataset, **kwargs)
            
        else:
            logger.error(f"Método de otimização '{metodo}' não suportado.")
            return {"status": "unsupported_method", "method": metodo}