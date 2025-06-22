import pytest
from unittest.mock import MagicMock, patch, call

# Assume the class is in src.N.avaliacao_continua.avaliacao_continua
from src.N.avaliacao_continua.avaliacao_continua import AvaliacaoContinua

# --- Fixtures for Mock Data and Dependencies ---

@pytest.fixture
def mock_resultados_llmrag_valid():
    """Simula a entrada da etapa LLM com RAG."""
    return [
        {
            "query": "O que é inteligência artificial?",
            "answer": "Inteligência artificial é um campo da ciência da computação.",
            "context_documents": ["Doc 1: IA é um campo...", "Doc 2: Outro texto sobre IA."]
        },
        {
            "query": "O que são redes neurais?",
            "answer": "Redes neurais são um subcampo do aprendizado de máquina.",
            "context_documents": ["Doc 3: Redes neurais são...", "Doc 4: Mais sobre redes."]
        },
        {
            "query": "Qual a capital da França?",
            "answer": "Não foi possível encontrar uma resposta no contexto fornecido.",
            "context_documents": []
        }
    ]

@pytest.fixture
def mock_referencias_valid():
    """Simula as respostas de referência (ground truth)."""
    return [
        {"query": "O que é inteligência artificial?", "answer": "IA é a área da computação que simula a inteligência humana."},
        {"query": "O que são redes neurais?", "answer": "Redes neurais são modelos computacionais inspirados no cérebro humano."},
        {"query": "Qual a capital da França?", "answer": "Paris é a capital da França."},
    ]

@pytest.fixture
def mock_evaluate_load():
    """Mocks the evaluate.load function."""
    mock_metric = MagicMock()
    mock_metric.compute.return_value = {"score": 0.8} # Generic score
    
    def load_side_effect(metric_name):
        if metric_name == "rouge":
            mock_metric.compute.return_value = {"rouge1": 0.5, "rouge2": 0.3, "rougeL": 0.4}
        elif metric_name == "bertscore":
            mock_metric.compute.return_value = {"precision": [0.7], "recall": [0.6], "f1": [0.65]}
        return mock_metric

    return MagicMock(side_effect=load_side_effect)

@pytest.fixture
def mock_llm_judge_call():
    """Mocks the internal LLM call for LLM-as-a-judge."""
    mock_llm_judge = MagicMock()
    mock_llm_judge.return_value = "Avaliação positiva do LLM."
    return mock_llm_judge

# --- Tests for AvaliacaoContinua ---

@patch('src.N.avaliacao_continua.avaliacao_continua.evaluate_load')
def test_init_success(mock_evaluate_load):
    """Test successful initialization and metric loading."""
    avaliador = AvaliacaoContinua()
    mock_evaluate_load.assert_has_calls([call("rouge"), call("bertscore")], any_order=True)
    assert 'rouge' in avaliador.metrics
    assert 'bertscore' in avaliador.metrics

@patch('src.N.avaliacao_continua.avaliacao_continua.evaluate_load', side_effect=Exception("Load error"))
def test_init_metric_load_failure(mock_evaluate_load):
    """Test initialization when metric loading fails."""
    with pytest.raises(Exception, match="Load error"): # Assuming it re-raises if both fail
        avaliador = AvaliacaoContinua()
    # If the class handles it gracefully (e.g., logs and continues), adjust this test
    # For example:
    # avaliador = AvaliacaoContinua()
    # assert 'rouge' not in avaliador.metrics
    # assert 'bertscore' not in avaliador.metrics

@patch('src.N.avaliacao_continua.avaliacao_continua.evaluate_load')
@patch('src.N.avaliacao_continua.avaliacao_continua.AvaliacaoContinua._evaluate_llm_as_judge')
def test_run_happy_path_with_references(mock_llm_judge_call, mock_evaluate_load_func,
                                        mock_resultados_llmrag_valid, mock_referencias_valid,
                                        mock_evaluate_load): # Use the fixture for evaluate_load
    """
    Test successful evaluation with both automatic metrics and LLM-as-a-judge, with references.
    """
    mock_evaluate_load_func.side_effect = mock_evaluate_load.side_effect # Use fixture's side_effect
    
    avaliador = AvaliacaoContinua()
    results = avaliador.run(mock_resultados_llmrag_valid, referencias=mock_referencias_valid)

    assert len(results) == len(mock_resultados_llmrag_valid)
    assert mock_llm_judge_call.call_count == len(mock_resultados_llmrag_valid)
    
    for item in results:
        assert "avaliacao_automatica" in item
        assert "avaliacao_llm_judge" in item
        assert "rouge" in item["avaliacao_automatica"]
        assert "bertscore" in item["avaliacao_automatica"]
        assert item["avaliacao_llm_judge"] == "Avaliação positiva do LLM." # Based on mock

    # Verify specific calls for automatic metrics
    mock_evaluate_load_func.assert_has_calls([
        call.compute(predictions=['Inteligência artificial é um campo da ciência da computação.'], references=['IA é a área da computação que simula a inteligência humana.']),
        call.compute(predictions=['Redes neurais são um subcampo do aprendizado de máquina.'], references=['Redes neurais são modelos computacionais inspirados no cérebro humano.']),
        call.compute(predictions=['Não foi possível encontrar uma resposta no contexto fornecido.'], references=['Paris é a capital da França.']),
    ], any_order=True)

@patch('src.N.avaliacao_continua.avaliacao_continua.evaluate_load')
@patch('src.N.avaliacao_continua.avaliacao_continua.AvaliacaoContinua._evaluate_llm_as_judge')
def test_run_without_references(mock_llm_judge_call, mock_evaluate_load_func,
                                mock_resultados_llmrag_valid, mock_evaluate_load):
    """
    Test evaluation when no references are provided.
    Automatic metrics requiring references should not be calculated or return empty.
    """
    mock_evaluate_load_func.side_effect = mock_evaluate_load.side_effect

    avaliador = AvaliacaoContinua()
    results = avaliador.run(mock_resultados_llmrag_valid, referencias=None)

    assert len(results) == len(mock_resultados_llmrag_valid)
    assert mock_llm_judge_call.call_count == len(mock_resultados_llmrag_valid)

    for item in results:
        assert "avaliacao_automatica" in item
        assert item["avaliacao_automatica"] == {} # Should be empty if no references
        assert "avaliacao_llm_judge" in item

@patch('src.N.avaliacao_continua.avaliacao_continua.evaluate_load')
@patch('src.N.avaliacao_continua.avaliacao_continua.AvaliacaoContinua._evaluate_llm_as_judge')
def test_run_empty_input(mock_llm_judge_call, mock_evaluate_load_func):
    """Test run with an empty list of LLM RAG results."""
    avaliador = AvaliacaoContinua()
    results = avaliador.run([])
    assert results == []
    mock_llm_judge_call.assert_not_called()
    mock_evaluate_load_func.assert_not_called()

@patch('src.N.avaliacao_continua.avaliacao_continua.evaluate_load')
@patch('src.N.avaliacao_continua.avaliacao_continua.AvaliacaoContinua._evaluate_llm_as_judge', side_effect=Exception("LLM Judge error"))
def test_run_llm_judge_failure(mock_llm_judge_call, mock_evaluate_load_func, mock_resultados_llmrag_valid, mock_referencias_valid, mock_evaluate_load):
    """Test that LLM-as-a-judge failure is handled gracefully."""
    mock_evaluate_load_func.side_effect = mock_evaluate_load.side_effect
    avaliador = AvaliacaoContinua()
    results = avaliador.run(mock_resultados_llmrag_valid, referencias=mock_referencias_valid)
    
    assert len(results) == len(mock_resultados_llmrag_valid)
    for item in results:
        assert "avaliacao_llm_judge" in item
        assert "LLM Judge error" in item["avaliacao_llm_judge"] # Or a specific error message/marker

# Add more test cases as needed:
# - Test _evaluate_automatic when a specific metric (e.g., ROUGE) fails.
# - Test with missing 'query' or 'answer' in input items.
# - Test citation precision (if implemented).