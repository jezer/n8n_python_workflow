import spacy
from typing import List, Dict, Any, Optional
import logging

class MetadadosEnriquecidos:
    """
    Extrai metadados via NER customizado (spaCy + transformer) e faz linking com entidades do grafo.
    Loga todos os metadados gerados.
    """

    def __init__(
        self, nlp=None, supabase_client=None,
        modelo_ner: str = "en_core_web_trf",
        entidades_grafo: Optional[List[str]] = None,
        log_level: int = logging.INFO
    ):
        self.nlp = nlp or spacy.load(modelo_ner)
        self.supabase = supabase_client or get_supabase_client()
        self.entidades_grafo = set(entidades_grafo) if entidades_grafo else set()
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("MetadadosEnriquecidos")

    def extrair_metadados(self, texto: str) -> List[Dict[str, Any]]:
        """
        Extrai entidades nomeadas do texto.
        """
        doc = self.nlp(texto)
        metadados = []
        for ent in doc.ents:
            metadado = {
                "texto": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char
            }
            metadados.append(metadado)
        return metadados

    def linking_entidades(self, metadados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Faz linking das entidades extraídas com entidades do grafo.
        """
        for m in metadados:
            m["linked"] = m["texto"] in self.entidades_grafo
        return metadados
    
    def salvar_no_supabase(self, tabela: str, dados: dict):
        try:
            resp = self.supabase.table(tabela).insert(dados).execute()
            return resp
        except Exception as e:
            self.logger.error(f"Erro ao salvar no Supabase: {e}")
    def run(self, documentos: List[Dict[str, Any]], grafo=None) -> List[Dict[str, Any]]:
        """
        Recebe lista de documentos (com 'conteudo' ou 'pergunta_gerada'/'resposta_gerada'), 
        extrai e enriquece metadados, faz linking com grafo.
        """
        # Se grafo for fornecido, extrai entidades do grafo para linking
        if grafo is not None:
            entidades = set()
            for s, p, o in grafo:
                entidades.add(str(s))
                entidades.add(str(o))
            self.entidades_grafo = entidades

        docs_enriquecidos = []
        for doc in documentos:
            # Preferencialmente usa 'pergunta_gerada'/'resposta_gerada', senão 'conteudo'
            texto = doc.get("pergunta_gerada") or doc.get("resposta_gerada") or doc.get("conteudo", "")
            metadados = self.extrair_metadados(texto)
            metadados_linkados = self.linking_entidades(metadados)
            self.logger.info(f"Metadados extraídos: {metadados_linkados}")
            doc_enriquecido = doc.copy()
            doc_enriquecido["metadados"] = metadados_linkados
            docs_enriquecidos.append(doc_enriquecido)
            # Salva cada metadado no Supabase
            for m in metadados_linkados:
                registro = {
                    "entidade": m["texto"],
                    "tipo": m["label"],
                    "documento_id": doc.get("id") or doc.get("nome_arquivo") or None
                }
                self.salvar_no_supabase("metadados_enriquecidos", registro)
        return docs_enriquecidos
