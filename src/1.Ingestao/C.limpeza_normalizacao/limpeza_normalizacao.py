import re
import unicodedata
import logging
from typing import List, Dict, Any, Optional

class LimpezaNormalizacao:
    """
    Limpeza e normalização de textos:
    - Remove cabeçalhos e rodapés (heurísticas e IA)
    - Normaliza encoding (UTF-8)
    - Remove lixo textual via classificador binário ou heurísticas
    - Logging estruturado e flexível
    - Permite configuração de padrões de cabeçalho/rodapé
    - Retorna opcionalmente documentos descartados
    """

    def __init__(
        self,
        classificador_binario=None,
        logger: Optional[logging.Logger] = None,
        padroes_cabecalho: Optional[List[str]] = None,
        padroes_rodape: Optional[List[str]] = None
    ):
        """
        classificador_binario: função ou objeto com método predict(texto) -> bool (True = lixo)
        logger: logger customizado (opcional)
        padroes_cabecalho/rodape: lista de regex para identificar linhas a remover
        """
        self.classificador_binario = classificador_binario
        self.logger = logger or logging.getLogger(__name__)
        self.padroes_cabecalho = padroes_cabecalho or [r'^(Página|Page|Copyright|Confidencial)']
        self.padroes_rodape = padroes_rodape or [r'^(Página|Page|Copyright|Confidencial)']

    def remover_cabecalho_rodape(self, texto: str) -> str:
        """
        Remove linhas iniciais/finais suspeitas de serem cabeçalho/rodapé.
        """
        linhas = texto.splitlines()
        # Remove até 2 linhas iniciais/finais se forem "suspeitas"
        while linhas and (len(linhas[0].strip()) < 10 or any(re.search(p, linhas[0], re.I) for p in self.padroes_cabecalho)):
            linhas.pop(0)
        while linhas and (len(linhas[-1].strip()) < 10 or any(re.search(p, linhas[-1], re.I) for p in self.padroes_rodape)):
            linhas.pop()
        return "\n".join(linhas)

    def normalizar_encoding(self, texto: str) -> str:
        """
        Remove caracteres não UTF-8, normaliza acentuação e remove caracteres de controle.
        """
        texto = unicodedata.normalize("NFKC", texto)
        texto = texto.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
        # Remove caracteres de controle (exceto \n e \t)
        texto = re.sub(r'[^\x09\x0A\x20-\x7E\xA0-\uFFFF]', '', texto)
        # Remove espaços duplicados
        texto = re.sub(r'[ \t]+', ' ', texto)
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        return texto.strip()

    def detectar_lixo(self, texto: str) -> bool:
        """
        Usa classificador binário se disponível, senão heurística:
        - Muito pouco texto
        - Muitos caracteres gráficos
        - Excesso de símbolos ou URLs isoladas
        """
        if self.classificador_binario:
            try:
                return self.classificador_binario.predict(texto)
            except Exception as e:
                self.logger.warning(f"Erro no classificador_binario: {e}")
        if len(texto.strip()) < 30:
            return True
        if re.search(r'[\u25A0-\u25FF]{3,}', texto):  # blocos de caracteres gráficos
            return True
        if re.search(r'(https?://\S+)', texto) and len(texto.strip()) < 60:
            return True
        if re.search(r'^[\W_]{10,}$', texto.strip()):
            return True
        return False

    def run(
        self,
        documentos: List[Dict[str, Any]],
        retornar_descartados: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Recebe lista de documentos (dicts com 'conteudo'), retorna lista limpa/normalizada.
        Se retornar_descartados=True, retorna (docs_limpos, docs_descartados).
        """
        docs_limpos = []
        docs_descartados = []
        for doc in documentos:
            texto = doc.get("conteudo", "")
            texto = self.normalizar_encoding(texto)
            texto = self.remover_cabecalho_rodape(texto)
            if not self.detectar_lixo(texto):
                doc_limpo = doc.copy()
                doc_limpo["conteudo"] = texto