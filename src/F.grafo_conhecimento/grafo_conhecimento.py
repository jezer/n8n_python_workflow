from typing import List, Dict, Any
import logging
import rdflib

class GrafoConhecimento:
    """
    Gera grafo de conhecimento a partir de chunks classificados.
    Extrai triplas (sujeito, predicado, objeto), normaliza entidades e monta grafo RDF.
    """

    def __init__(self, namespace: str = "http://example.org/", log_level: int = logging.INFO):
        self.namespace = namespace
        self.grafo = rdflib.Graph()
        self.ns = rdflib.Namespace(namespace)
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("GrafoConhecimento")

    def extrair_triplas(self, chunk: str) -> List[Dict[str, str]]:
        """
        Extrai triplas do texto do chunk.
        (Stub: substitua por modelo REBEL ou similar)
        """
        # Exemplo: retorna uma tripla dummy se encontrar "é um"
        triplas = []
        if "é um" in chunk:
            partes = chunk.split("é um")
            sujeito = partes[0].strip().split()[-1]
            objeto = partes[1].strip().split()[0]
            triplas.append({"sujeito": sujeito, "predicado": "é_um", "objeto": objeto})
        return triplas

    def normalizar_entidade(self, entidade: str) -> str:
        """
        Normaliza entidades (ex: Python3 → Python 3).
        """
        return entidade.replace("Python3", "Python 3").strip()

    def adicionar_triplas_ao_grafo(self, triplas: List[Dict[str, str]]):
        for tripla in triplas:
            s = self.ns[self.normalizar_entidade(tripla["sujeito"])]
            p = self.ns[tripla["predicado"]]
            o = self.ns[self.normalizar_entidade(tripla["objeto"])]
            self.grafo.add((s, p, o))

    def run(self, documentos: List[Dict[str, Any]]) -> rdflib.Graph:
        """
        Recebe lista de documentos (com 'chunks_classificados'), extrai e adiciona triplas ao grafo.
        """
        for doc in documentos:
            chunks = doc.get("chunks_classificados", [])
            if not isinstance(chunks, list):
                self.logger.warning(f"Documento sem lista de chunks_classificados: {doc}")
                continue            
            for chunk_info in doc.get("chunks_classificados", []):
                chunk = chunk_info["chunk"] if isinstance(chunk_info, dict) else chunk_info
                triplas = self.extrair_triplas(chunk)
                self.adicionar_triplas_ao_grafo(triplas)
        self.logger.info(f"Grafo gerado com {len(self.grafo)} triplas.")
        return self.grafo
        
    def exportar_rdf(self, caminho: str = "grafo.rdf", formato: str = "xml"):
        self.grafo.serialize(destination=caminho, format=formato)
        self.logger.info(f"Grafo exportado para {caminho} ({formato})")