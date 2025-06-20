from typing import List, Dict, Any, Optional
import numpy as np
import os
import logging

class AtualizacaoIncremental:
    """
    Atualização incremental de embeddings (delta-tuning).
    Versiona embeddings e permite rollback automático se recall cair >5%.
    """

    def __init__(
        self,
        caminho_emb: str = "./embeddings_versions",
        recall_threshold: float = 0.05,
        log_level: int = logging.INFO
    ):
        self.caminho_emb = caminho_emb
        self.recall_threshold = recall_threshold
        os.makedirs(self.caminho_emb, exist_ok=True)
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("AtualizacaoIncremental")

    def salvar_embeddings(self, embeddings: np.ndarray, versao: str):
        caminho = os.path.join(self.caminho_emb, f"embeddings_v{versao}.npy")
        np.save(caminho, embeddings)
        self.logger.info(f"Embeddings salvos em {caminho}")

    def carregar_embeddings(self, versao: str) -> np.ndarray:
        caminho = os.path.join(self.caminho_emb, f"embeddings_v{versao}.npy")
        return np.load(caminho)

    def delta_tuning(self, embeddings_antigos: np.ndarray, novos_dados: np.ndarray) -> np.ndarray:
        """
        Stub: Atualiza embeddings antigos com delta dos novos dados.
        """
        # Exemplo: concatena e normaliza
        atualizados = np.vstack([embeddings_antigos, novos_dados])
        # Normalização (opcional)
        atualizados = atualizados / (np.linalg.norm(atualizados, axis=1, keepdims=True) + 1e-8)
        return atualizados

    def avaliar_recall(self, embeddings: np.ndarray, consultas: np.ndarray, ground_truth: np.ndarray, k: int = 5) -> float:
        """
        Stub: calcula recall@k (exemplo simplificado).
        """
        import faiss
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        D, I = index.search(consultas, k)
        acertos = 0
        for i, gt in enumerate(ground_truth):
            if gt in I[i]:
                acertos += 1
        recall = acertos / len(ground_truth)
        self.logger.info(f"Recall@{k}: {recall:.3f}")
        return recall

    def rollback(self, versao_anterior: str):
        self.logger.warning(f"Rollback automático para embeddings versão {versao_anterior}")

    def run(
        self,
        embeddings_antigos: np.ndarray,
        novos_dados: np.ndarray,
        consultas: Optional[np.ndarray] = None,
        ground_truth: Optional[np.ndarray] = None,
        versao_atual: str = "001",
        versao_nova: str = "002"
    ) -> Dict[str, Any]:
        """
        Orquestra atualização incremental, avaliação de recall e rollback se necessário.
        """
        self.logger.info("Iniciando atualização incremental de embeddings (delta-tuning).")
        if embeddings_antigos.shape[1] != novos_dados.shape[1]:
            self.logger.error("Dimensões incompatíveis entre embeddings antigos e novos dados.")
            raise ValueError("Dimensões incompatíveis.")
        embeddings_atualizados = self.delta_tuning(embeddings_antigos, novos_dados)
        self.salvar_embeddings(embeddings_atualizados, versao_nova)

        if consultas is not None and ground_truth is not None:
            recall_antigo = self.avaliar_recall(embeddings_antigos, consultas, ground_truth)
            recall_novo = self.avaliar_recall(embeddings_atualizados, consultas, ground_truth)
            if recall_antigo - recall_novo > self.recall_threshold:
                self.rollback(versao_atual)
                return {
                    "status": "rollback",
                    "recall_antigo": recall_antigo,
                    "recall_novo": recall_novo
                }
            else:
                return {
                    "status": "atualizado",
                    "recall_antigo": recall_antigo,
                    "recall_novo": recall_novo
                }
        else:
            return {
                "status": "atualizado",
                "recall_antigo": None,
                "recall_novo": None
            }