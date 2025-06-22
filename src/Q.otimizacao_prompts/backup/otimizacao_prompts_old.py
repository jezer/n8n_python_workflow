from typing import List, Dict, Any, Optional
import logging
import random

class OtimizacaoPrompts:
    """
    Otimização de prompts via A/B test e técnicas como STaR.
    Loga todas as variações e impactos.
    """

    def __init__(
        self,
        templates: Optional[List[str]] = None,
        llm_client=None,  # Deve ter método generate(prompt) -> resposta
        avaliador=None,   # Deve ter método avaliar(resposta) -> score
        log_level: int = logging.INFO
    ):
        self.templates = templates or [
            "Responda de forma objetiva: {pergunta}",
            "Explique passo a passo: {pergunta}",
            "Responda como um especialista: {pergunta}",
            "Forneça uma resposta detalhada: {pergunta}"
        ]
        self.llm_client = llm_client or self._stub_llm
        self.avaliador = avaliador or self._stub_avaliador
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("OtimizacaoPrompts")

    def _stub_llm(self, prompt: str) -> str:
        return "Resposta gerada automaticamente (stub)."

    def _stub_avaliador(self, resposta: str) -> float:
        return random.uniform(0, 1)

    def ab_test(self, pergunta: str) -> Dict[str, Any]:
        """
        Realiza A/B test entre diferentes templates de prompt para uma pergunta.
        """
        resultados = []
        for template in self.templates:
            prompt = template.format(pergunta=pergunta)
            resposta = self.llm_client(prompt)
            score = self.avaliador(resposta)
            resultados.append({
                "template": template,
                "prompt": prompt,
                "resposta": resposta,
                "score": score
            })
            self.logger.info(f"Template testado: {template} | Score: {score:.3f}")
        melhor = max(resultados, key=lambda x: x["score"])
        return {
            "pergunta": pergunta,
            "resultados": resultados,
            "melhor_template": melhor["template"],
            "melhor_score": melhor["score"]
        }

    def star_optimization(self, pergunta: str, n_iter: int = 3) -> Dict[str, Any]:
        """
        Técnica STaR: gera raciocínio intermediário, ajusta prompt e avalia impacto.
        """
        historico = []
        melhor_score = -1
        melhor_prompt = ""
        for i in range(n_iter):
            raciocinio = f"Raciocine sobre: {pergunta} (iteração {i+1})"
            prompt = f"{raciocinio}\n{random.choice(self.templates).format(pergunta=pergunta)}"
            resposta = self.llm_client(prompt)
            score = self.avaliador(resposta)
            historico.append({
                "prompt": prompt,
                "resposta": resposta,
                "score": score
            })
            self.logger.info(f"STaR iteração {i+1}: Score {score:.3f}")
            if score > melhor_score:
                melhor_score = score
                melhor_prompt = prompt
        return {
            "pergunta": pergunta,
            "historico": historico,
            "melhor_prompt": melhor_prompt,
            "melhor_score": melhor_score
        }
        
    def run(self, resultados_avaliacao: List[Dict[str, Any]], metodo: str = "ab_test") -> List[Dict[str, Any]]:
        """
        Recebe lista de avaliações, executa otimização de prompts para cada pergunta.
        """
        otimizacoes = []
        for item in resultados_avaliacao:
            pergunta = item.get("query", "")
            if not pergunta:
                self.logger.warning("Item sem 'query': %s", item)
                continue
            try:
                if metodo == "ab_test":
                    resultado = self.ab_test(pergunta)
                elif metodo == "star":
                    resultado = self.star_optimization(pergunta)
                else:
                    raise ValueError("Método de otimização não suportado.")
                otimizacoes.append(resultado)
            except Exception as e:
                self.logger.error(f"Erro ao otimizar prompt para '{pergunta}': {e}")
        return otimizacoes
        