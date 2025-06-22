import pytest
from unittest.mock import MagicMock, patch
from main import etapa_limpeza

# Mock input data for etapa_limpeza (simulating output from etapa_segmentacao)
mock_resultados_segmentados = [
    {
        "nome_arquivo": "doc1.txt",
        "segmentos": ["  Primeiro segmento com espaços extras.  ", "SEGUNDO SEGMENTO EM MAIÚSCULAS.\n", "Terceiro\tsegmento com tabulação."]
    },
    {
        "nome_arquivo": "doc2.txt",
        "segmentos": []  # Documento sem segmentos
    },
    {
        "nome_arquivo": "doc3.txt",
        "segmentos": ["Um único segmento normal, sem necessidade de limpeza aparente."]
    }
]

# Mock output data that LimpezaNormalizacao().run() would produce
# This represents the data after cleaning and normalization.
# The exact nature of cleaning (e.g., lowercasing, stripping) would depend on
# the actual implementation of LimpezaNormalizacao.
mock_cleaned_data_expected_from_run = [
    {
        "nome_arquivo": "doc1.txt",
        "segmentos": ["primeiro segmento com espaços extras.", "segundo segmento em maiúsculas.", "terceiro segmento com tabulação."] # Example: cleaned
    },
    {
        "nome_arquivo": "doc2.txt",
        "segmentos": []
    },
    {
        "nome_arquivo": "doc3.txt",
        "segmentos": ["um único segmento normal, sem necessidade de limpeza aparente."] # Example: cleaned
    }
]

@patch('main.LimpezaNormalizacao')
def test_etapa_limpeza_happy_path(mock_limpeza_normalizacao_class):
    """
    Testa o fluxo principal da etapa_limpeza com entrada válida.
    Verifica se LimpezaNormalizacao é instanciada, seu método run é chamado,
    e o resultado é retornado corretamente.
    """
    # Configure o mock da classe LimpezaNormalizacao e seu método run
    mock_instance = MagicMock()
    mock_limpeza_normalizacao_class.return_value = mock_instance
    mock_instance.run.return_value = mock_cleaned_data_expected_from_run

    # Execute a função a ser testada
    resultados = etapa_limpeza(mock_resultados_segmentados)

    # Verifique se LimpezaNormalizacao foi instanciada
    mock_limpeza_normalizacao_class.assert_called_once()

    # Verifique se o método run foi chamado com os dados segmentados corretos
    mock_instance.run.assert_called_once_with(mock_resultados_segmentados)

    # Verifique se o resultado da etapa_limpeza é o que o mock de run retornou
    assert resultados == mock_cleaned_data_expected_from_run
    assert len(resultados) == len(mock_resultados_segmentados)

@patch('main.LimpezaNormalizacao')
def test_etapa_limpeza_empty_input_list(mock_limpeza_normalizacao_class):
    """
    Testa a etapa_limpeza com uma lista de entrada vazia.
    """
    mock_instance = MagicMock()
    mock_limpeza_normalizacao_class.return_value = mock_instance
    mock_instance.run.return_value = [] # Esperado que run retorne lista vazia para entrada vazia

    resultados = etapa_limpeza([])

    mock_limpeza_normalizacao_class.assert_called_once()
    mock_instance.run.assert_called_once_with([])
    assert resultados == []

@patch('main.LimpezaNormalizacao')
def test_etapa_limpeza_doc_with_empty_segments(mock_limpeza_normalizacao_class):
    """
    Testa a etapa_limpeza com um documento que possui uma lista de segmentos vazia.
    """
    input_doc_empty_segments = [{"nome_arquivo": "empty_segs.txt", "segmentos": []}]
    expected_output_for_empty_segments = [{"nome_arquivo": "empty_segs.txt", "segmentos": []}] # Assumindo que a estrutura é mantida

    mock_instance = MagicMock()
    mock_limpeza_normalizacao_class.return_value = mock_instance
    mock_instance.run.return_value = expected_output_for_empty_segments

    resultados = etapa_limpeza(input_doc_empty_segments)

    mock_limpeza_normalizacao_class.assert_called_once()
    mock_instance.run.assert_called_once_with(input_doc_empty_segments)
    assert resultados == expected_output_for_empty_segments

# Nota: Para testes "completos" do arquivo limpeza_normalizacao.py em si,
# seria necessário o código fonte de LimpezaNormalizacao e as instruções
# específicas de teste (testeinstrucoes.md). Os testes acima focam na integração
# da etapa_limpeza dentro do main.py.