from typing import List, Dict, Any, Optional
import logging

class GeracaoQA:
    """
    Geração de perguntas e respostas (QA) usando LLM especializado (ex: GPT-4) com chain-of-thought e few-shot.
    """

    def __init__(
        self,
        llm_client=None,  # Deve ter método generate(prompt) -> resposta
        exemplos_few_shot: Optional[List[Dict[str, str]]] = None,
        max_pergunta: int = 3,
        log_level: int = logging.INFO
    ):
        self.llm_client = llm_client or self._stub_llm
        self.exemplos_few_shot = exemplos_few_shot or [
            {"pergunta": "O que é Python?", "resposta": "Python é uma linguagem de programação."},
            {"pergunta": "Para que serve o FAISS?", "resposta": "FAISS é usado para busca vetorial eficiente."}
        ]
        self.max_pergunta = max_pergunta
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("GeracaoQA")

    def _stub_llm(self, prompt: str) -> str:
        # Stub: retorna resposta dummy
        return "Resposta gerada automaticamente (stub)."

    def montar_prompt(self, tripla: Dict[str, str]) -> str:
        exemplos = "\n".join(
            [f"Q: {ex['pergunta']}\nA: {ex['resposta']}" for ex in self.exemplos_few_shot]
        )
        chain_of_thought = (
            f"Considere a tripla: ({tripla['sujeito']}, {tripla['predicado']}, {tripla['objeto']}). "
            "Pense passo a passo e gere uma pergunta relevante e sua resposta, seguindo o padrão dos exemplos."
        )
        return f"{exemplos}\n\n{chain_of_thought}\nQ:"

    def gerar_qa_para_tripla(self, tripla: Dict[str, str]) -> Dict[str, str]:
        prompt = self.montar_prompt(tripla)
        resposta = self.llm_client(prompt)
        return {
            "tripla": tripla,
            "pergunta_gerada": prompt.split('\nQ:')[-1].strip(),
            "resposta_gerada": resposta
        }

     def run(self, grafo: Any) -> List[Dict[str, Any]]:
        """
        Recebe grafo (rdflib.Graph), gera QA para até max_pergunta triplas por domínio.
        """
        qas = []
        triplas = []
        for s, p, o in grafo:
            if not all([s, p, o]):
                self.logger.warning(f"Tripla incompleta: {(s, p, o)}")
                continue
            triplas.append({
                "sujeito": str(s),
                "predicado": str(p),
                "objeto": str(o)
            })
        for tripla in triplas[:self.max_pergunta]:
            try:
                qa = self.gerar_qa_para_tripla(tripla)
                qas.append(qa)
                self.logger.info(f"QA gerado para tripla: {tripla}")
            except Exception as e:
                self.logger.error(f"Erro ao gerar QA para tripla {tripla}: {e}")
        return qas