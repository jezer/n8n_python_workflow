import pytest
from unittest.mock import MagicMock, patch
from main import etapa_chunking

# Mock input data for etapa_chunking (simulating output from etapa_limpeza)
mock_resultados_limpos = [
    {
        "nome_arquivo": "doc1.txt",
        "segmentos": ["Este é o primeiro segmento já limpo e normalizado.", "Este é o segundo segmento, também processado."]
    },
    {
        "nome_arquivo": "doc2.txt",
        "segmentos": ["Um único segmento longo o suficiente para ser dividido em múltiplos chunks pelo processo de chunking inteligente."]
    },
    {
        "nome_arquivo": "doc3.txt",
        "segmentos": [] # Documento com segmentos limpos, mas a lista de segmentos está vazia
    }
]

# Mock output data that ChunkingInteligente().run() would produce.
# The structure of "chunks" (e.g., texto_chunk, metadados_chunk) is an assumption,
# as the actual implementation of ChunkingInteligente is not provided.
# This mock data represents a plausible output after chunking.
mock_chunked_data_expected_from_run = [
    {
        "nome_arquivo": "doc1.txt",
        "chunks": [
            {"texto_chunk": "Este é o primeiro segmento", "metadados_chunk": {"origem_segmento_idx": 0, "token_count": 5}},
            {"texto_chunk": "já limpo e normalizado.", "metadados_chunk": {"origem_segmento_idx": 0, "token_count": 4}},
            {"texto_chunk": "Este é o segundo segmento,", "metadados_chunk": {"origem_segmento_idx": 1, "token_count": 5}},
            {"texto_chunk": "também processado.", "metadados_chunk": {"origem_segmento_idx": 1, "token_count": 2}}
        ]
    },
    {
        "nome_arquivo": "doc2.txt",
        "chunks": [
            {"texto_chunk": "Um único segmento longo o suficiente", "metadados_chunk": {"origem_segmento_idx": 0, "token_count": 6}},
            {"texto_chunk": "para ser dividido em múltiplos chunks", "metadados_chunk": {"origem_segmento_idx": 0, "token_count": 6, "overlap_prev": True}},
            {"texto_chunk": "pelo processo de chunking inteligente.", "metadados_chunk": {"origem_segmento_idx": 0, "token_count": 5, "overlap_prev": True}}
        ]
    },
    {
        "nome_arquivo": "doc3.txt",
        "chunks": [] # Esperado que um documento sem segmentos resulte em zero chunks
    }
]

@patch('main.ChunkingInteligente')
def test_etapa_chunking_happy_path(mock_chunking_inteligente_class):
    """
    Testa o fluxo principal da etapa_chunking com entrada válida.
    Verifica se ChunkingInteligente é instanciada, seu método run é chamado,
    e o resultado é retornado corretamente.
    """
    mock_instance = MagicMock()
    mock_chunking_inteligente_class.return_value = mock_instance
    mock_instance.run.return_value = mock_chunked_data_expected_from_run

    resultados = etapa_chunking(mock_resultados_limpos)

    mock_chunking_inteligente_class.assert_called_once()
    mock_instance.run.assert_called_once_with(mock_resultados_limpos)
    assert resultados == mock_chunked_data_expected_from_run
    assert len(resultados) == len(mock_resultados_limpos)

@patch('main.ChunkingInteligente')
def test_etapa_chunking_empty_input_list(mock_chunking_inteligente_class):
    """
    Testa a etapa_chunking com uma lista de entrada vazia.
    """
    mock_instance = MagicMock()
    mock_chunking_inteligente_class.return_value = mock_instance
    mock_instance.run.return_value = [] # Esperado que run retorne lista vazia para entrada vazia

    resultados = etapa_chunking([])

    mock_chunking_inteligente_class.assert_called_once()
    mock_instance.run.assert_called_once_with([])
    assert resultados == []

# Nota: Para testes "completos" do arquivo chunking_inteligente.py em si,
# seria necessário o código fonte de ChunkingInteligente e as instruções
# específicas de teste (testeinstrucoes.md). Os testes acima focam na integração
# da etapa_chunking dentro do main.py.
#
# Se a classe ChunkingInteligente tivesse lógica complexa para lidar com
# documentos com "segmentos" vazios (ex: doc3 no mock_resultados_limpos),
# o mock_instance.run.return_value para esse caso específico poderia ser ajustado
# no teste de happy_path ou em um teste dedicado.
# Por ora, mock_chunked_data_expected_from_run cobre esse cenário.