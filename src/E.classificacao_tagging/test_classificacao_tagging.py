import pytest
from unittest.mock import MagicMock, patch
from main import etapa_classificacao

# Mock input data for etapa_classificacao (simulating output from etapa_chunking)
mock_resultados_chunking = [
    {
        "nome_arquivo": "doc1.txt",
        "chunks": [
            {"texto_chunk": "Este é o primeiro chunk do doc1.", "metadados_chunk": {"id": "d1c1", "origem_segmento_idx": 0}},
            {"texto_chunk": "Segundo chunk, um pouco diferente.", "metadados_chunk": {"id": "d1c2", "origem_segmento_idx": 1}}
        ]
    },
    {
        "nome_arquivo": "doc2.txt",
        "chunks": [
            {"texto_chunk": "Chunk único do documento 2.", "metadados_chunk": {"id": "d2c1", "origem_segmento_idx": 0}}
        ]
    },
    {
        "nome_arquivo": "doc3.txt",
        "chunks": []  # Documento sem chunks
    }
]

# Mock output data that ClassificacaoTagging().run() would produce.
# This represents the data after classification and tagging.
# Based on fluxo.mmd, chunks might get a classification and tags like 'REVISAR'.
mock_classificados_data_expected_from_run = [
    {
        "nome_arquivo": "doc1.txt",
        "chunks": [
            {"texto_chunk": "Este é o primeiro chunk do doc1.", "metadados_chunk": {"id": "d1c1", "origem_segmento_idx": 0}, "classificacao": "Tipo A", "tags": ["importante"], "confianca": 0.9},
            {"texto_chunk": "Segundo chunk, um pouco diferente.", "metadados_chunk": {"id": "d1c2", "origem_segmento_idx": 1}, "classificacao": "Tipo B", "tags": ["REVISAR", "sensivel"], "confianca": 0.65}
        ]
    },
    {
        "nome_arquivo": "doc2.txt",
        "chunks": [
            {"texto_chunk": "Chunk único do documento 2.", "metadados_chunk": {"id": "d2c1", "origem_segmento_idx": 0}, "classificacao": "Tipo A", "tags": [], "confianca": 0.98}
        ]
    },
    {
        "nome_arquivo": "doc3.txt",
        "chunks": []  # Documento sem chunks permanece sem chunks
    }
]

@patch('main.ClassificacaoTagging')
def test_etapa_classificacao_happy_path(mock_classificacao_tagging_class):
    """
    Testa o fluxo principal da etapa_classificacao com entrada válida.
    Verifica se ClassificacaoTagging é instanciada, seu método run é chamado,
    e o resultado é retornado corretamente.
    """
    mock_instance = MagicMock()
    mock_classificacao_tagging_class.return_value = mock_instance
    mock_instance.run.return_value = mock_classificados_data_expected_from_run

    resultados = etapa_classificacao(mock_resultados_chunking)

    mock_classificacao_tagging_class.assert_called_once()
    mock_instance.run.assert_called_once_with(mock_resultados_chunking)
    assert resultados == mock_classificados_data_expected_from_run
    assert len(resultados) == len(mock_resultados_chunking)

@patch('main.ClassificacaoTagging')
def test_etapa_classificacao_empty_input_list(mock_classificacao_tagging_class):
    """
    Testa a etapa_classificacao com uma lista de entrada vazia.
    """
    mock_instance = MagicMock()
    mock_classificacao_tagging_class.return_value = mock_instance
    mock_instance.run.return_value = []  # Esperado que run retorne lista vazia para entrada vazia

    resultados = etapa_classificacao([])

    mock_classificacao_tagging_class.assert_called_once()
    mock_instance.run.assert_called_once_with([])
    assert resultados == []

@patch('main.ClassificacaoTagging')
def test_etapa_classificacao_doc_with_no_chunks(mock_classificacao_tagging_class):
    """
    Testa a etapa_classificacao com um documento que não possui chunks.
    """
    input_doc_no_chunks = [{"nome_arquivo": "no_chunks.txt", "chunks": []}]
    # Espera-se que a estrutura seja mantida, e run() retorne o doc com chunks vazios
    expected_output_for_no_chunks = [{"nome_arquivo": "no_chunks.txt", "chunks": []}]

    mock_instance = MagicMock()
    mock_classificacao_tagging_class.return_value = mock_instance
    mock_instance.run.return_value = expected_output_for_no_chunks

    resultados = etapa_classificacao(input_doc_no_chunks)

    mock_classificacao_tagging_class.assert_called_once()
    mock_instance.run.assert_called_once_with(input_doc_no_chunks)
    assert resultados == expected_output_for_no_chunks

# Nota: Para testes "completos" do arquivo classificacao_tagging.py em si,
# seria necessário o código fonte de ClassificacaoTagging e as instruções
# específicas de teste (testeinstrucoes.md). Os testes acima focam na integração
# da etapa_classificacao dentro do main.py.