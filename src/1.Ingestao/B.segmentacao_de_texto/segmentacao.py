import re
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from unidecode import unidecode

# Importações opcionais separadas para feedback mais claro
try:
    import spacy
except ImportError:
    spacy = None

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    RecursiveCharacterTextSplitter = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    import numpy as np
except ImportError:
    np = None

class SegmentadorUnificado:
    """
    Classe unificada para segmentação avançada de texto.
    Inclui:
    - Segmentação por tamanho fixo
    - Segmentação semântica (embeddings)
    - Segmentação por tópicos (NLP)
    - Segmentação hierárquica (legal, científica, automática)
    - Processamento em lote de arquivos markdown
    - Salvamento dos segmentos em JSON
    """

    def __init__(
        self,
        spacy_model: str = 'pt_core_news_sm',
        embedder_model: str = 'paraphrase-multilingual-MiniLM-L12-v2',
        classificador_binario: Optional[Any] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Inicializa o SegmentadorUnificado.
        Permite injeção de classificador IA e logger para facilitar testes.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.classificador_binario = classificador_binario
        self.nlp = None
        self.embedder = None
        self.text_splitter = None

        if spacy and spacy_model:
            try:
                self.nlp = spacy.load(spacy_model)
            except Exception:
                self.logger.warning(f"spaCy model '{spacy_model}' não encontrado.")
        else:
            if not spacy:
                self.logger.warning("spaCy não está instalado.")

        if SentenceTransformer and embedder_model:
            try:
                self.embedder = SentenceTransformer(embedder_model)
            except Exception:
                self.logger.warning(f"Embedder model '{embedder_model}' não encontrado.")
        else:
            if not SentenceTransformer:
                self.logger.warning("sentence-transformers não está instalado.")

        if RecursiveCharacterTextSplitter:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, length_function=len, add_start_index=True
            )
        else:
            self.logger.warning("langchain.text_splitter não está instalado.")

    def segmentar_heuristica(self, texto: str) -> List[Dict]:
        """
        Segmentação simples por parágrafo como fallback.
        """
        if not isinstance(texto, str) or not texto.strip():
            self.logger.warning("Texto vazio ou não-string recebido em segmentar_heuristica.")
            return []
        return [{"text": p, "method": "heuristica"} for p in texto.split('\n\n') if p.strip()]

    def _calc_start_end(self, text: str, chunk_text: str, prev_end: int = 0) -> (int, int):
        """
        Função utilitária para calcular índices de início e fim de um chunk.
        """
        start = text.find(chunk_text, prev_end)
        end = start + len(chunk_text)
        return start, end

    def chunk_by_size(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict]:
        """
        Segmentação por tamanho fixo usando LangChain.
        """
        if not self.text_splitter:
            raise Exception("LangChain text_splitter não disponível.")
        self.text_splitter._chunk_size = chunk_size
        self.text_splitter._chunk_overlap = overlap
        chunks = self.text_splitter.create_documents([text])
        result = []
        for chunk in chunks:
            start, end = self._calc_start_end(text, chunk.page_content, result[-1]['end'] if result else 0)
            result.append({
                "text": chunk.page_content,
                "start": start,
                "end": end,
                "method": "fixed_size"
            })
        return result

    def semantic_chunking(self, text: str, threshold: float = 0.85) -> List[Dict]:
        """
        Segmentação semântica usando embeddings.
        """
        if not self.embedder or not np:
            raise Exception("SentenceTransformer ou numpy não disponível.")
        paragraphs = [p for p in text.split('\n') if p.strip()]
        if len(paragraphs) < 2:
            return [{"text": text, "method": "semantic", "start": 0, "end": len(text)}]
        embeddings = self.embedder.encode(paragraphs, convert_to_tensor=True)
        clusters = []
        current_cluster = [0]
        for i in range(1, len(paragraphs)):
            similarity = float(np.dot(embeddings[i-1], embeddings[i]))
            if similarity >= threshold:
                current_cluster.append(i)
            else:
                clusters.append(current_cluster)
                current_cluster = [i]
        if current_cluster:
            clusters.append(current_cluster)
        chunks = []
        prev_end = 0
        for cluster in clusters:
            chunk_text = '\n'.join(paragraphs[i] for i in cluster)
            start, end = self._calc_start_end(text, chunk_text, prev_end)
            prev_end = end
            chunks.append({
                "text": chunk_text,
                "start": start,
                "end": end,
                "method": "semantic",
                "num_paragraphs": len(cluster)
            })
        return chunks

    def topic_aware_chunking(self, text: str, max_chunk_size: int = 1500) -> List[Dict]:
        """
        Segmentação por tópicos usando spaCy.
        """
        if not self.nlp:
            raise Exception("spaCy não disponível.")
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        chunks = []
        current_chunk = []
        current_length = 0
        prev_end = 0
        for idx, sent in enumerate(sentences):
            sent_length = len(sent)
            # Corrigido: analisar a sentença atual, não só as primeiras 50 do doc
            is_topic_boundary = any(
                token.text in ('Mas', 'Porém', 'No entanto', 'Além disso', 'Por outro lado')
                for token in self.nlp(sent)
            )
            if (current_length + sent_length > max_chunk_size) or is_topic_boundary:
                if current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    start, end = self._calc_start_end(text, chunk_text, prev_end)
                    prev_end = end
                    chunks.append({
                        "text": chunk_text,
                        "method": "topic_aware",
                        "boundary": is_topic_boundary,
                        "start": start,
                        "end": end
                    })
                    current_chunk = []
                    current_length = 0
            current_chunk.append(sent)
            current_length += sent_length
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            start, end = self._calc_start_end(text, chunk_text, prev_end)
            chunks.append({
                "text": chunk_text,
                "method": "topic_aware",
                "start": start,
                "end": end
            })
        return chunks

    def hierarchical_segmentation(self, text: str, strategy: str = "auto") -> List[Dict]:
        """
        Segmentação hierárquica baseada em padrões de títulos.
        """
        if not isinstance(text, str) or not text.strip():
            self.logger.warning("Texto vazio ou não-string recebido em hierarchical_segmentation.")
            return []
        if strategy == "legal":
            sections = re.split(r'\n\s*(ARTIGO|CAPÍTULO|SEÇÃO|§|Parágrafo único)\s+', text)
        elif strategy == "scientific":
            sections = re.split(r'\n\s*(ABSTRACT|RESUMO|1\s?\.|INTRODUCTION|INTRODUÇÃO)\s+', text)
        else:
            # Regex melhorado para evitar cortes errados em títulos em caixa alta
            sections = re.split(r'\n\s*([A-Z][A-Z\s]{2,}\n|-{3,}|_{3,})\s*', text)
        sections = [s for s in sections if s and len(s.strip()) > 50]
        chunks = []
        prev_end = 0
        for section in sections:
            if len(section) > 2000:
                sub_chunks = self.semantic_chunking(section)
                for chunk in sub_chunks:
                    chunk['hierarchy'] = 2
                    chunk['strategy'] = strategy
                chunks.extend(sub_chunks)
            else:
                start, end = self._calc_start_end(text, section, prev_end)
                prev_end = end
                chunks.append({
                    "text": section,
                    "method": "hierarchical",
                    "hierarchy": 1,
                    "strategy": strategy,
                    "start": start,
                    "end": end
                })
        return chunks

    def segment(self, text: str, method: str = "auto", **kwargs) -> List[Dict]:
        """
        Método principal de segmentação.
        """
        if not isinstance(text, str) or not text.strip():
            self.logger.warning("Texto vazio ou não-string recebido em segment.")
            return []
        if method == "fixed" or len(text) <= 1500:
            return self.chunk_by_size(text, **kwargs)
        elif method == "semantic":
            return self.semantic_chunking(text, **kwargs)
        elif method == "topic":
            return self.topic_aware_chunking(text, **kwargs)
        elif method == "hierarchical":
            return self.hierarchical_segmentation(text, **kwargs)
        else:  # auto
            if len(text) > 10000:
                return self.hierarchical_segmentation(text, strategy="auto")
            elif len(text) > 3000:
                return self.semantic_chunking(text)
            else:
                return self.chunk_by_size(text)

    def process_directory(self, input_path: str, output_path: Optional[str] = None, method: str = "auto"):
        """
        Processa todos os arquivos markdown em um diretório, segmentando e salvando em JSON.
        """
        input_dir = Path(input_path)
        output_dir = Path(output_path) if output_path else None
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        for file in input_dir.glob("*.md"):
            content = file.read_text(encoding="utf-8")
            segments = self.segment(content, method=method)
            if output_dir:
                out_file = output_dir / f"{file.stem}_segments.json"
                import json
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(segments, f, ensure_ascii=False, indent=2)
            else:
                print(f"Arquivo: {file.name} - {len(segments)} segmentos")

    def segmentar_documento(self, texto: str, classificador=None, logger=None) -> List[Dict]:
        """
        Segmenta um documento usando classificador IA se disponível, com fallback heurístico.
        """
        logger = logger or self.logger
        classificador = classificador or self.classificador_binario
        if not isinstance(texto, str) or not texto.strip():
            logger.warning("Texto vazio ou não-string recebido em segmentar_documento.")
            return []
        try:
            if not classificador or not hasattr(classificador, "segmentar"):
                raise Exception("Classificador IA não disponível ou inválido.")
            segmentos = classificador.segmentar(texto)
            logger.info("Segmentação IA aplicada.")
            return [{"text": s, "method": "ia"} for s in segmentos if s.strip()]
        except Exception as e:
            logger.warning(f"Falha IA, usando heurística: {e}")
            return self.segmentar_heuristica(texto)