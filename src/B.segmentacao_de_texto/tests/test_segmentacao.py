import pytest
import logging
from B.segmentacao_de_texto.segmentacao import SegmentadorUnificado

class MockClassificador:
    def segmentar(self, texto):
        return texto.split('\n\n')

@pytest.fixture
def segmentador():
    logger = logging.getLogger("pytest_segmentador")
    return SegmentadorUnificado(
        classificador_binario=MockClassificador(),
        logger=logger
    )

@pytest.mark.parametrize("texto,esperado", [
    ("Primeiro parágrafo.\n\nSegundo parágrafo.\n\nTerceiro parágrafo.", 3),
    ("Apenas um parágrafo.", 1),
    ("", 0),
])
def test_segmentar_heuristica(segmentador, texto, esperado):
    segmentos = segmentador.segmentar_heuristica(texto)
    assert len(segmentos) == esperado
    for s in segmentos:
        assert s["method"] == "heuristica"

def test_segmentar_documento_ia(segmentador):
    texto = "Primeiro parágrafo.\n\nSegundo parágrafo."
    segmentos = segmentador.segmentar_documento(texto)
    assert len(segmentos) == 2
    for s in segmentos:
        assert s["method"] == "ia"

def test_segmentar_documento_fallback(segmentador):
    segmentador.classificador_binario = None
    texto = "Primeiro parágrafo.\n\nSegundo parágrafo."
    segmentos = segmentador.segmentar_documento(texto)
    assert len(segmentos) == 2
    for s in segmentos:
        assert s["method"] == "heuristica"

def test_segmentar_documento_vazio(segmentador):
    segmentos = segmentador.segmentar_documento("")
    assert segmentos == []

def test_segmentar_um_paragrafo(segmentador):
    segmentos = segmentador.segmentar_documento("Apenas um parágrafo.")
    assert len(segmentos) == 1

def test_segmentar_rodape(segmentador):
    texto = "Primeiro parágrafo.\n\nPágina 1"
    segmentos = segmentador.segmentar_heuristica(texto)
    assert any("Página" in s["text"] for s in segmentos)

def test_chunk_by_size(segmentador):
    if segmentador.text_splitter:
        texto = "A" * 5000
        segmentos = segmentador.chunk_by_size(texto, chunk_size=1000, overlap=0)
        assert len(segmentos) >= 4
        for s in segmentos:
            assert s["method"] == "fixed_size"

def test_semantic_chunking(segmentador):
    if segmentador.embedder and segmentador.nlp and segmentador.text_splitter:
        texto = "\n".join([f"Parágrafo {i}" for i in range(10)])
        segmentos = segmentador.semantic_chunking(texto)
        assert len(segmentos) >= 1
        for s in segmentos:
            assert s["method"] == "semantic"

def test_topic_aware_chunking(segmentador):
    if segmentador.nlp:
        texto = "Introdução. Mas agora outro tópico. Além disso, mais um."
        segmentos = segmentador.topic_aware_chunking(texto)
        assert len(segmentos) >= 1
        for s in segmentos:
            assert s["method"] == "topic_aware"

def test_hierarchical_segmentation(segmentador):
    texto = "CAPÍTULO 1\nConteúdo do capítulo 1.\n\nCAPÍTULO 2\nConteúdo do capítulo 2."
    segmentos = segmentador.hierarchical_segmentation(texto, strategy="legal")
    assert len(segmentos) >= 2
    for s in segmentos:
        assert s["method"] == "hierarchical"

def test_segment_auto(segmentador):
    texto = "A" * 2000
    segmentos = segmentador.segment(texto)
    assert isinstance(segmentos, list)
    for s in segmentos:
        assert s["method"] in ("fixed_size", "semantic", "hierarchical")