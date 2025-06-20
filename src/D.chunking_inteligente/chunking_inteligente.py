import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import logging

class ChunkingInteligente:
    """
    Chunking semântico com sliding window (512 tokens) e overlap de 15%.
    Usa embeddings para determinar pontos de corte naturais e valida chunks com modelo de confiança.
    Chunks inválidos (score < 0.7) recebem tag 'REVISAR' e são logados.
    """

    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        window_size: int = 512,
        overlap: float = 0.15,
        confidence_model=None,  # Ex: DeBERTa-v3, stub por padrão
        log_level: int = logging.INFO
    ):
        self.window_size = window_size
        self.overlap = overlap
        self.embedding_model = SentenceTransformer(embedding_model)
        self.confidence_model = confidence_model  # Deve ter método predict_proba(chunk) -> float
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("ChunkingInteligente")

    def _split_sliding_window(self, texto: str) -> List[str]:
        tokens = texto.split()
        step = int(self.window_size * (1 - self.overlap))
        chunks = []
        for i in range(0, len(tokens), step):
            chunk = tokens[i:i + self.window_size]
            if chunk:
                chunks.append(" ".join(chunk))
        return chunks

    def _cluster_chunks(self, chunks: List[str]) -> List[List[str]]:
        # Gera embeddings e clusteriza para agrupar por tópicos naturais
        if len(chunks) < 3:
            return [chunks]
        embeddings = self.embedding_model.encode(chunks)
        n_clusters = max(1, len(chunks) // 3)
        clustering = AgglomerativeClustering(n_clusters=n_clusters)
        labels = clustering.fit_predict(embeddings)
        agrupados = [[] for _ in range(n_clusters)]
        for idx, label in enumerate(labels):
            agrupados[label].append(chunks[idx])
        return agrupados

    def _validar_chunks(self, chunks: List[str]) -> List[Dict[str, Any]]:
        resultados = []
        for chunk in chunks:
            score = 1.0
            if self.confidence_model:
                score = float(self.confidence_model.predict_proba([chunk])[0][1])
            valido = score >= 0.7
            tag = None if valido else "REVISAR"
            if not valido:
                self.logger.warning(f"Chunk inválido (score={score:.2f}): {chunk[:80]}...")
            resultados.append({
                "chunk": chunk,
                "score_confianca": score,
                "valido": valido,
                "tag": tag
            })
        return resultados

    def run(self, documentos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recebe lista de documentos (dicts com 'conteudo'), retorna lista com chunks validados.
        """
        docs_chunked = []
        for doc in documentos:
            texto = doc.get("conteudo", "")
            if not texto:
                self.logger.warning(f"Documento sem conteúdo: {doc}")
                continue
            chunks = self._split_sliding_window(texto)
            agrupados = self._cluster_chunks(chunks)
            # Ajusta tamanho dos chunks para manter contexto (concatena grupos)
            chunks_finais = [" ".join(grupo) for grupo in agrupados]
            chunks_validados = self._validar_chunks(chunks_finais)
            doc_chunked = doc.copy()
            doc_chunked["chunks"] = chunks_validados
            docs_chunked.append(doc_chunked)
        return docs_chunked
