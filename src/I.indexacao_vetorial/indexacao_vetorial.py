import faiss
import numpy as np
import os
import logging
from typing import List, Dict, Any, Optional

class IndexacaoVetorial:
    """
    Indexação vetorial usando FAISS (HNSW, IVF-PQ).
    Permite balancear recall vs velocidade e versionar índices.
    """

    def __init__(
        self,
        metodo: str = "HNSW",
        dim: int = 768,
        caminho_indice: str = "./faiss_indices",
        versionar: bool = True,
        log_level: int = logging.INFO
    ):
        self.metodo = metodo.upper()
        self.dim = dim
        self.caminho_indice = caminho_indice
        self.versionar = versionar
        os.makedirs(self.caminho_indice, exist_ok=True)
        self.indice = None
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("IndexacaoVetorial")

    def construir_indice(self, embeddings: np.ndarray):
        if self.metodo == "HNSW":
            self.indice = faiss.IndexHNSWFlat(self.dim, 32)
            self.indice.hnsw.efConstruction = 200
        elif self.metodo == "IVF-PQ":
            nlist = 100
            m = 16
            quantizer = faiss.IndexFlatL2(self.dim)
            self.indice = faiss.IndexIVFPQ(quantizer, self.dim, nlist, m, 8)
            self.indice.train(embeddings)
        else:
            raise ValueError(f"Método de indexação não suportado: {self.metodo}")
        self.indice.add(embeddings)
        self.logger.info(f"Índice {self.metodo} criado com {embeddings.shape[0]} vetores.")

    def salvar_indice(self, versao: Optional[str] = None):
        if self.indice is None:
            raise RuntimeError("Índice não criado.")
        nome = f"faiss_{self.metodo.lower()}"
        if self.versionar and versao:
            nome += f"_v{versao}"
        caminho = os.path.join(self.caminho_indice, nome + ".index")
        faiss.write_index(self.indice, caminho)
        self.logger.info(f"Índice salvo em {caminho}")

    def carregar_indice(self, versao: Optional[str] = None):
        nome = f"faiss_{self.metodo.lower()}"
        if self.versionar and versao:
            nome += f"_v{versao}"
        caminho = os.path.join(self.caminho_indice, nome + ".index")
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Índice não encontrado: {caminho}")
        self.indice = faiss.read_index(caminho)
        self.logger.info(f"Índice carregado de {caminho}")

    def buscar(self, consultas: np.ndarray, k: int = 5) -> Dict[str, Any]:
        if self.indice is None:
            raise RuntimeError("Índice não carregado.")
        D, I = self.indice.search(consultas, k)
        return {"distancias": D, "indices": I}

    def monitorar_recall(self, consultas: np.ndarray, ground_truth: np.ndarray, k: int = 5) -> float:
        """
        Calcula recall@k para monitoramento do índice.
        """
        resultados = self.buscar(consultas, k)
        acertos = 0
        for i, gt in enumerate(ground_truth):
            if gt in resultados["indices"][i]:
                acertos += 1
        recall = acertos / len(ground_truth)
        self.logger.info(f"Recall@{k}: {recall:.3f}")
        return recall
        
    def run(self, dados: List[Dict[str, Any]], versao: Optional[str] = None) -> None:
        """
        Recebe lista de dicts com 'embedding', constrói e salva índice.
        """
        if not isinstance(dados, list) or not dados:
            self.logger.error("Entrada para run() deve ser uma lista não vazia de dicionários.")
            raise ValueError("Entrada deve ser uma lista não vazia de dicionários.")
        embeddings = np.array([d["embedding"] for d in dados if "embedding" in d])
        if embeddings.shape[1] != self.dim:
            self.logger.error(f"Dimensão dos embeddings ({embeddings.shape[1]}) não bate com o esperado ({self.dim}).")
            raise ValueError("Dimensão dos embeddings incompatível.")
        self.construir_indice(embeddings)
        self.salvar_indice(versao=versao)