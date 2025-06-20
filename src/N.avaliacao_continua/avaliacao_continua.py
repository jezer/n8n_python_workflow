from typing import List, Dict, Any, Optional
import logging

class AvaliacaoContinua:
    """
    Avaliação automática de respostas usando ROUGE, BERTScore e LLM-as-a-judge.
    Permite avaliação humana (stub).
    """

    def __init__(
        self,
        llm_judge=None,  # Deve ter método judge(prompt) -> avaliação
        rouge_scorer=None,
        bert_scorer=None,
        log_level: int = logging.INFO
    ):
        from rouge_score import rouge_scorer as rs
        import bert_score
        self.rouge_scorer = rouge_scorer or rs.RougeScorer(['rougeL'], use_stemmer=True)
        self.bert_scorer = bert_scorer or bert_score.BERTScorer(lang="pt", rescale_with_baseline=True)
        self.llm_judge = llm_judge or self._stub_llm_judge
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("AvaliacaoContinua")

    def _stub_llm_judge(self, prompt: str) -> str:
        return "Avaliação LLM-as-a-judge (stub): resposta plausível."

    def avaliar_automatico(self, referencia: str, resposta: str) -> Dict[str, Any]:
        rouge = self.rouge_scorer.score(referencia, resposta)
        P, R, F1 = self.bert_scorer.score([resposta], [referencia])
        return {
            "rougeL": rouge["rougeL"].fmeasure,
            "bertscore_P": float(P[0]),
            "bertscore_R": float(R[0]),
            "bertscore_F1": float(F1[0])
        }

    def avaliar_llm_judge(self, referencia: str, resposta: str, criterios: Optional[str] = None) -> str:
        prompt = (
            f"Referência: {referencia}\n"
            f"Resposta do modelo: {resposta}\n"
            f"Criterios de avaliação: {criterios or 'clareza, factualidade, completude'}\n"
            "Avalie a resposta do modelo segundo os critérios acima, de forma objetiva."
        )
        return self.llm_judge(prompt)

    def avaliar_humano(self, referencia: str, resposta: str) -> str:
        # Stub: integração futura com painel de avaliação humana
        return "Avaliação humana pendente."

    def run(self, resultados_llmrag: List[Dict[str, Any]], referencias: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Recebe lista de dicts com 'query', 'resposta', 'prompt', etc.
        Se referências forem fornecidas, avalia automaticamente e via LLM-as-a-judge.
        """
        avaliacoes = []
        for i, item in enumerate(resultados_llmrag):
            query = item.get("query", "")
            resposta = item.get("resposta", "")
            referencia = (referencias[i] if referencias and i < len(referencias) else "")
            if not query or not resposta:
                self.logger.warning(f"Item malformado: {item}")
                continue
            auto = self.avaliar_automatico(referencia, resposta) if referencia else {}
            llm = self.avaliar_llm_judge(referencia, resposta)
            humano = self.avaliar_humano(referencia, resposta)
            avaliacao = {
                "query": query,
                "resposta": resposta,
                "referencia": referencia,
                "avaliacao_automatica": auto,
                "avaliacao_llm_judge": llm,
                "avaliacao_humana": humano
            }
            self.logger.info(f"Avaliação gerada para query: {query}")
            avaliacoes.append(avaliacao)
        return avaliacoes