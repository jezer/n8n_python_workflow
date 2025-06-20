import pytest
from unittest.mock import MagicMock, patch, call
from main import etapa_grafo_conhecimento

# Mock input data for etapa_grafo_conhecimento (simulating output from etapa_classificacao)
mock_resultados_classificados = [
    {
        "nome_arquivo": "doc1.txt",
        "chunks": [
            {"texto_chunk": "Conteúdo do chunk 1 de doc1.", "classificacao": "Tipo A", "tags": ["importante"]},
            {"texto_chunk": "Conteúdo do chunk 2 de doc1.", "classificacao": "Tipo B", "tags": ["REVISAR"]}
        ]
    },
    {
        "nome_arquivo": "doc2.txt",
        "chunks": [
            {"texto_chunk": "Conteúdo do chunk único de doc2.", "classificacao": "Tipo A", "tags": []}
        ]
    }
]

# Mock output from GrafoConhecimento().run() - a list of triples (s, p, o)
mock_grafo_obj_triples = [
    ("Entidade1", "temPropriedade", "Valor1"),
    ("Entidade2", "relacionaCom", "Entidade3"),
    ("Doc1Chunk1", "menciona", "Entidade1")
]

@patch('main.salvar_no_supabase')
@patch('main.GrafoConhecimento')
def test_etapa_grafo_conhecimento_happy_path(mock_grafo_conhecimento_class, mock_salvar_supabase):
    """
    Testa o fluxo principal da etapa_grafo_conhecimento com entrada válida.
    Verifica instanciação, chamadas de método, exportação e salvamento no Supabase.
    """
    mock_grafo_instance = MagicMock()
    mock_grafo_conhecimento_class.return_value = mock_grafo_instance
    mock_grafo_instance.run.return_value = mock_grafo_obj_triples

    # Execute a função a ser testada
    resultado_grafo = etapa_grafo_conhecimento(mock_resultados_classificados)

    # Verificações
    mock_grafo_conhecimento_class.assert_called_once()
    mock_grafo_instance.run.assert_called_once_with(mock_resultados_classificados)
    mock_grafo_instance.exportar_rdf.assert_called_once_with("grafo.rdf")

    assert mock_salvar_supabase.call_count == len(mock_grafo_obj_triples)
    expected_supabase_calls = []
    for s, p, o in mock_grafo_obj_triples:
        registro = {"sujeito": str(s), "predicado": str(p), "objeto": str(o)}
        expected_supabase_calls.append(call("triplas_grafo", registro))
    mock_salvar_supabase.assert_has_calls(expected_supabase_calls, any_order=False)

    assert resultado_grafo == mock_grafo_obj_triples

@patch('main.salvar_no_supabase')
@patch('main.GrafoConhecimento')
def test_etapa_grafo_conhecimento_sem_triplas_geradas(mock_grafo_conhecimento_class, mock_salvar_supabase):
    """
    Testa o caso onde GrafoConhecimento().run() retorna uma lista vazia de triplas.
    """
    mock_grafo_instance = MagicMock()
    mock_grafo_conhecimento_class.return_value = mock_grafo_instance
    mock_grafo_instance.run.return_value = []  # Nenhuma tripla gerada

    resultado_grafo = etapa_grafo_conhecimento(mock_resultados_classificados)

    mock_grafo_conhecimento_class.assert_called_once()
    mock_grafo_instance.run.assert_called_once_with(mock_resultados_classificados)
    mock_grafo_instance.exportar_rdf.assert_called_once_with("grafo.rdf") # Exportação ainda deve ocorrer

    mock_salvar_supabase.assert_not_called() # Nenhuma tripla para salvar

    assert resultado_grafo == []

@patch('main.salvar_no_supabase')
@patch('main.GrafoConhecimento')
def test_etapa_grafo_conhecimento_input_vazio(mock_grafo_conhecimento_class, mock_salvar_supabase):
    """
    Testa a etapa_grafo_conhecimento com uma lista de entrada vazia.
    """
    mock_grafo_instance = MagicMock()
    mock_grafo_conhecimento_class.return_value = mock_grafo_instance
    # Assumindo que run() retorna lista vazia para entrada vazia
    mock_grafo_instance.run.return_value = []

    input_vazio = []
    resultado_grafo = etapa_grafo_conhecimento(input_vazio)

    mock_grafo_conhecimento_class.assert_called_once()
    mock_grafo_instance.run.assert_called_once_with(input_vazio)
    mock_grafo_instance.exportar_rdf.assert_called_once_with("grafo.rdf")

    mock_salvar_supabase.assert_not_called()

    assert resultado_grafo == []

@patch('main.salvar_no_supabase')
@patch('main.GrafoConhecimento')
def test_etapa_grafo_conhecimento_falha_supabase(mock_grafo_conhecimento_class, mock_salvar_supabase):
    """
    Testa o comportamento quando salvar_no_supabase levanta uma exceção.
    A função deve continuar e retornar o grafo_obj.
    """
    mock_grafo_instance = MagicMock()
    mock_grafo_conhecimento_class.return_value = mock_grafo_instance
    mock_grafo_instance.run.return_value = mock_grafo_obj_triples
    mock_salvar_supabase.side_effect = Exception("Falha ao salvar no Supabase")

    # A exceção de salvar_no_supabase não deve impedir a função de retornar o grafo.
    # (Considerar se a função deveria tratar essa exceção ou deixá-la propagar)
    # Por ora, o teste verifica que a função completa e retorna o grafo_obj.
    resultado_grafo = etapa_grafo_conhecimento(mock_resultados_classificados)
    assert resultado_grafo == mock_grafo_obj_triples
    assert mock_salvar_supabase.call_count > 0 # Verifica que tentou salvar

# Nota: Para testes "completos" do arquivo grafo_conhecimento.py em si,
# seria necessário o código fonte de GrafoConhecimento e as instruções
# específicas de teste (testeinstrucoes.md). Os testes acima focam na integração
# da etapa_grafo_conhecimento dentro do main.py.