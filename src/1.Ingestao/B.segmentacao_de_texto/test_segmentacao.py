import pytest
from unittest.mock import MagicMock, patch

# Assuming the import path in main.py should be corrected to B.segmentacao_de_texto
# If the path in main.py is correct (B.segmentacao_segmentacao_de_texto),
# you might need to adjust the import and patch paths accordingly.
from main import etapa_segmentacao

# Mock data for testing
mock_input_docs = [
    {"nome_arquivo": "doc1.txt", "conteudo": "Este é o primeiro parágrafo.\n\nEste é o segundo parágrafo."},
    {"nome_arquivo": "doc2.txt", "conteudo": "Conteúdo do documento 2."},
    {"nome_arquivo": "doc3.txt", "conteudo": "Documento com\nvárias\nlinhas."},
]

# Expected output structure after segmentation (mocked)
mock_segmented_output = [
    {"nome_arquivo": "doc1.txt", "segmentos": ["Este é o primeiro parágrafo.", "Este é o segundo parágrafo."]},
    {"nome_arquivo": "doc2.txt", "segmentos": ["Conteúdo do documento 2."]},
    {"nome_arquivo": "doc3.txt", "segmentos": ["Documento com\nvárias\nlinhas."]},
]

@patch('main.SegmentadorUnificado')
def test_etapa_segmentacao_happy_path(mock_segmentador_class):
    """
    Testa o fluxo principal da etapa_segmentacao com entrada válida.
    """
    # Configure o mock do SegmentadorUnificado e seu método segment
    mock_instance = MagicMock()
    mock_segmentador_class.return_value = mock_instance

    # Configure o retorno do método segment para cada documento de entrada
    # Note: This assumes a simple mapping. For more complex scenarios,
    # you might need side_effect or check call arguments.
    def mock_segment_side_effect(content, method="auto"):
        if content == mock_input_docs[0]["conteudo"]:
            return mock_segmented_output[0]["segmentos"]
        elif content == mock_input_docs[1]["conteudo"]:
            return mock_segmented_output[1]["segmentos"]
        elif content == mock_input_docs[2]["conteudo"]:
            return mock_segmented_output[2]["segmentos"]
        return [] # Default return for unexpected content

    mock_instance.segment.side_effect = mock_segment_side_effect

    # Execute a função a ser testada
    resultados = etapa_segmentacao(mock_input_docs)

    # Verifique se o SegmentadorUnificado foi instanciado
    mock_segmentador_class.assert_called_once()

    # Verifique se o método segment foi chamado para cada documento
    assert mock_instance.segment.call_count == len(mock_input_docs)
    mock_instance.segment.assert_any_call(mock_input_docs[0]["conteudo"], method="auto")
    mock_instance.segment.assert_any_call(mock_input_docs[1]["conteudo"], method="auto")
    mock_instance.segment.assert_any_call(mock_input_docs[2]["conteudo"], method="auto")

    # Verifique o formato e conteúdo da saída
    assert isinstance(resultados, list)
    assert len(resultados) == len(mock_input_docs)

    # Compare os resultados com a saída esperada (pode precisar de ordenação se a ordem não for garantida)
    # Assuming order is preserved based on input order
    assert resultados == mock_segmented_output

@patch('main.SegmentadorUnificado')
def test_etapa_segmentacao_empty_input(mock_segmentador_class):
    """
    Testa a etapa_segmentacao com uma lista de documentos vazia.
    """
    mock_instance = MagicMock()
    mock_segmentador_class.return_value = mock_instance

    resultados = etapa_segmentacao([])

    # Verifique se o SegmentadorUnificado foi instanciado (pode variar dependendo da implementação real)
    # Se a função não processa lista vazia, a instância pode não ser criada.
    # Assumindo que a instância é criada mesmo para lista vazia, mas segment não é chamado.
    mock_segmentador_class.assert_called_once()

    # Verifique se o método segment não foi chamado
    mock_instance.segment.assert_not_called()

    # Verifique se a saída é uma lista vazia
    assert isinstance(resultados, list)
    assert len(resultados) == 0
    assert resultados == []

@patch('main.SegmentadorUnificado')
def test_etapa_segmentacao_document_with_empty_content(mock_segmentador_class):
    """
    Testa a etapa_segmentacao com um documento cujo conteúdo está vazio.
    """
    input_docs = [{"nome_arquivo": "empty.txt", "conteudo": ""}]
    expected_output = [{"nome_arquivo": "empty.txt", "segmentos": []}] # Assuming segment returns [] for empty input

    mock_instance = MagicMock()
    mock_segmentador_class.return_value = mock_instance
    mock_instance.segment.return_value = [] # Mock segment to return empty list for empty content

    resultados = etapa_segmentacao(input_docs)

    # Verifique se o SegmentadorUnificado foi instanciado
    mock_segmentador_class.assert_called_once()

    # Verifique se o método segment foi chamado com o conteúdo vazio
    mock_instance.segment.assert_called_once_with("", method="auto")

    # Verifique a saída
    assert isinstance(resultados, list)
    assert len(resultados) == 1
    assert resultados == expected_output
