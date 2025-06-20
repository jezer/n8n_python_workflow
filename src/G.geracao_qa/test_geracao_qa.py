import pytest
from unittest.mock import MagicMock, patch
from src.G.geracao_qa.geracao_qa import GeracaoQA

# Mock input data simulating output from the knowledge graph step
mock_resultados_grafo = [
    {"head": "Entidade1", "relation": "temPropriedade", "tail": "Valor1"},
    {"head": "Entidade2", "relation": "relacionaCom", "tail": "Entidade3"},
    {"head": "Doc1Chunk1", "relation": "menciona", "tail": "Entidade1"}
]

# Mock output data that GeracaoQA().run() would produce
mock_qa_pairs = [
    {"pergunta_gerada": "Qual propriedade da Entidade1?", "resposta_gerada": "Valor1", "tripla": mock_resultados_grafo[0]},
    {"pergunta_gerada": "Com quem a Entidade2 se relaciona?", "resposta_gerada": "Entidade3", "tripla": mock_resultados_grafo[1]},
    {"pergunta_gerada": "O que o Doc1Chunk1 menciona?", "resposta_gerada": "Entidade1", "tripla": mock_resultados_grafo[2]}
]

@patch('src.G.geracao_qa.geracao_qa.GeracaoQA._generate_qa')  # Mock the LLM call
def test_geracao_qa_happy_path(mock_generate_qa):
    """
    Test the main flow of QA generation with valid input.
    """
    mock_generate_qa.side_effect = lambda triple: next(
        (qa_pair for qa_pair in mock_qa_pairs if qa_pair["tripla"] == triple),
        {"pergunta_gerada": "Pergunta padrão", "resposta_gerada": "Resposta padrão"}
    )

    qa_generator = GeracaoQA()
    resultados = qa_generator.run(mock_resultados_grafo)

    assert isinstance(resultados, list)
    assert len(resultados) == len(mock_resultados_grafo)
    for i, resultado in enumerate(resultados):
        assert resultado["pergunta_gerada"] is not None
        assert resultado["resposta_gerada"] is not None
        assert resultado["tripla"] == mock_resultados_grafo[i]

    assert mock_generate_qa.call_count == len(mock_resultados_grafo)

@patch('src.G.geracao_qa.geracao_qa.GeracaoQA._generate_qa')
def test_geracao_qa_empty_input(mock_generate_qa):
    """
    Test with an empty list of triples.
    """
    qa_generator = GeracaoQA()
    resultados = qa_generator.run([])

    assert isinstance(resultados, list)
    assert len(resultados) == 0
    mock_generate_qa.assert_not_called()

@patch('src.G.geracao_qa.geracao_qa.GeracaoQA._generate_qa')
def test_geracao_qa_generate_qa_returns_none(mock_generate_qa):
    """
    Test when the _generate_qa method returns None for some triples.
    """
    mock_generate_qa.return_value = None  # Simulate LLM returning None
    qa_generator = GeracaoQA()
    resultados = qa_generator.run(mock_resultados_grafo)

    assert isinstance(resultados, list)
    assert len(resultados) == len(mock_resultados_grafo)
    for resultado in resultados:
        assert resultado["pergunta_gerada"] is None
        assert resultado["resposta_gerada"] is None
        assert "tripla" in resultado
    assert mock_generate_qa.call_count == len(mock_resultados_grafo)

@patch('src.G.geracao_qa.geracao_qa.GeracaoQA._generate_qa')
def test_geracao_qa_with_exception_in_generate_qa(mock_generate_qa):
    """
    Test when the _generate_qa method raises an exception.
    """
    mock_generate_qa.side_effect = Exception("LLM call failed")
    qa_generator = GeracaoQA()

    # The run method should handle exceptions and return a default value
    resultados = qa_generator.run(mock_resultados_grafo)

    assert isinstance(resultados, list)
    assert len(resultados) == len(mock_resultados_grafo)
    for resultado in resultados:
        assert resultado["pergunta_gerada"] is None
        assert resultado["resposta_gerada"] is None
        assert "tripla" in resultado
    assert mock_generate_qa.call_count == len(mock_resultados_grafo)

# Add more test cases as needed, e.g.:
# - Test with different types of triples
# - Test with a large number of triples
# - Test the few-shot prompting logic (if implemented and configurable)
# - Test any factuality checks or chain-of-thought logic (if implemented)