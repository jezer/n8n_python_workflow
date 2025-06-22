from typing import List, Dict, Any
import logging

class ClassificacaoTagging:
    """
    Classificação multi-label de chunks usando modelo fine-tuned (ex: DeBERTa-v3).
    Chunks com score < 0.7 recebem tag 'REVISAR'.
    """

    def __init__(
        self,
        modelo_classificador=None,  # Deve ter método predict_proba(texto) -> Dict[label, score]
        labels: List[str] = None,
        threshold: float = 0.7,
        log_level: int = logging.INFO
    ):
        self.modelo_classificador = modelo_classificador or self._stub_model
        self.labels = labels or ["Fato", "Opinião", "Citação", "Dado", "Outro"]
        self.threshold = threshold
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("ClassificacaoTagging")

    def _stub_model(self, texto: str) -> Dict[str, float]:
        # Stub: atribui score aleatório para cada label
        import random
        return {label: random.uniform(0.5, 1.0) for label in self.labels}

    def classificar_chunk(self, chunk: str) -> Dict[str, Any]:
        scores = self.modelo_classificador(chunk)
        tags = [label for label, score in scores.items() if score >= self.threshold]
        revisar = any(score < self.threshold for score in scores.values())
        if revisar:
            tags.append("REVISAR")
            self.logger.warning(f"Chunk marcado para revisão: {chunk[:80]}...")
        return {
            "chunk": chunk,
            "tags": tags,
            "scores": scores
        }

    def run(self, documentos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recebe lista de documentos (cada doc com 'chunks'), retorna lista com chunks classificados e tags.
        """
        docs_classificados = []
        for doc in documentos:
            chunks = doc.get("chunks", [])
            if not isinstance(chunks, list):
                self.logger.warning(f"Documento sem lista de chunks: {doc}")
                continue
            chunks_classificados = []
            for chunk_info in chunks:
                chunk_text = chunk_info["chunk"] if isinstance(chunk_info, dict) else chunk_info
                if not isinstance(chunk_text, str) or not chunk_text.strip():
                    self.logger.warning(f"Chunk inválido: {chunk_info}")
                    continue
                resultado = self.classificar_chunk(chunk_text)
                chunks_classificados.append(resultado)
            doc_classificado = doc.copy()
            doc_classificado["chunks_classificados"] = chunks_classificados
            docs_classificados.append(doc_classificado)
        return docs_classificados


