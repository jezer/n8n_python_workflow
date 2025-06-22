import pytest
from unittest.mock import MagicMock, patch, call
import numpy as np

# Assume the class is in src.O.retriever_adaptativo.retriever_adaptativo
from src.O.retriever_adaptativo.retriever_adaptativo import RetrieverAdaptativo

# --- Fixtures for Mock Data ---

@pytest.fixture
def mock_evaluation_results_mixed():
    """
    Simulates input from the continuous evaluation step, with mixed results.
    """
    return [
        # Happy Path: Good ROUGE, positive LLM Judge
        {
            "query": "O que é inteligência artificial?",
            "answer": "Inteligência artificial é um campo da ciência da computação.",
            "context_documents": ["Doc IA"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.9}},
            "avaliacao_llm_judge": "Excelente resposta, concisa e precisa."
        },
        # Hard Negative 1: Low ROUGE
        {
            "query": "Detalhes sobre redes neurais.",
            "answer": "Redes neurais são um subcampo do aprendizado de máquina.",
            "context_documents": ["Doc Redes"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.3}}, # Below default threshold 0.5
            "avaliacao_llm_judge": "Boa resposta, mas poderia ser mais detalhada."
        },
        # Hard Negative 2: Negative LLM Judge feedback
        {
            "query": "Qual a capital da França?",
            "answer": "Não foi possível encontrar uma resposta no contexto fornecido.",
            "context_documents": [],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.1}},
            "avaliacao_llm_judge": "Resposta genérica, indica falta de informação no contexto."
        },
        # Hard Negative 3: Answer indicates failure
        {
            "query": "Explique o teorema de Bayes.",
            "answer": "Não sei a resposta para essa pergunta.",
            "context_documents": ["Doc Bayes"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.2}},
            "avaliacao_llm_judge": "Resposta curta e sem conteúdo."
        },
        # Borderline Case: ROUGE just above threshold
        {
            "query": "O que é aprendizado de máquina?",
            "answer": "Aprendizado de máquina é um ramo da IA.",
            "context_documents": ["Doc ML"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.55}}, # Above default threshold
            "avaliacao_llm_judge": "Resposta aceitável."
        },
        # Item with missing query/answer (should be skipped)
        {
            "answer": "Resposta sem query.",
            "context_documents": ["Doc Missing"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.1}},
            "avaliacao_llm_judge": "Missing query."
        },
        {
            "query": "Query sem resposta.",
            "context_documents": ["Doc Missing"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.1}},
            "avaliacao_llm_judge": "Missing answer."
        }
    ]

@pytest.fixture
def mock_evaluation_results_all_good():
    """All results are good, no hard negatives."""
    return [
        {
            "query": "O que é inteligência artificial?",
            "answer": "Inteligência artificial é um campo da ciência da computação.",
            "context_documents": ["Doc IA"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.9}},
            "avaliacao_llm_judge": "Excelente resposta, concisa e precisa."
        },
        {
            "query": "O que são redes neurais?",
            "answer": "Redes neurais são um subcampo do aprendizado de máquina.",
            "context_documents": ["Doc Redes"],
            "avaliacao_automatica": {"rouge": {"rougeL": 0.8}},
            "avaliacao_llm_judge": "Boa resposta, relevante ao contexto."
        }
    ]

# --- Tests for RetrieverAdaptativo ---

def test_retriever_adaptativo_init():
    """Test successful initialization."""
    adaptador = RetrieverAdaptativo(negative_mining_threshold=0.4)
    assert adaptador.negative_mining_threshold == 0.4

@patch('src.O.retriever_adaptativo.retriever_adaptativo.RetrieverAdaptativo._trigger_fine_tuning')
def test_run_happy_path_identifies_hard_negatives(mock_trigger_fine_tuning, mock_evaluation_results_mixed):
    """
    Test that run method correctly identifies hard negatives and triggers fine-tuning.
    """
    adaptador = RetrieverAdaptativo(negative_mining_threshold=0.5) # Default threshold
    results = adaptador.run(mock_evaluation_results_mixed)

    assert results["status"] == "adaptation_process_completed"
    assert results["num_hard_negatives"] == 3 # Based on mock_evaluation_results_mixed (excluding missing QA)
    assert len(results["hard_negatives_identified"]) == 3

    # Verify the identified hard negatives
    hard_neg_queries = [hn["query"] for hn in results["hard_negatives_identified"]]
    assert "Detalhes sobre redes neurais." in hard_neg_queries
    assert "Qual a capital da França?" in hard_neg_queries
    assert "Explique o teorema de Bayes." in hard_neg_queries
    assert "O que é inteligência artificial?" not in hard_neg_queries
    assert "O que é aprendizado de máquina?" not in hard_neg_queries

    mock_trigger_fine_tuning.assert_called_once()
    assert len(mock_trigger_fine_tuning.call_args[0][0]) == 3 # Ensure it's called with 3 hard negatives

@patch('src.O.retriever_adaptativo.retriever_adaptativo.RetrieverAdaptativo._trigger_fine_tuning')
def test_run_no_hard_negatives(mock_trigger_fine_tuning, mock_evaluation_results_all_good):
    """
    Test that no hard negatives are identified and fine-tuning is not triggered
    when all evaluation results are good.
    """
    adaptador = RetrieverAdaptativo(negative_mining_threshold=0.5)
    results = adaptador.run(mock_evaluation_results_all_good)

    assert results["status"] == "adaptation_process_completed"
    assert results["num_hard_negatives"] == 0
    assert len(results["hard_negatives_identified"]) == 0

    mock_trigger_fine_tuning.assert_called_once() # Still called, but with empty list
    assert len(mock_trigger_fine_tuning.call_args[0][0]) == 0

@patch('src.O.retriever_adaptativo.retriever_adaptativo.RetrieverAdaptativo._trigger_fine_tuning')
def test_run_empty_input(mock_trigger_fine_tuning):
    """
    Test run method with an empty list of evaluation results.
    """
    adaptador = RetrieverAdaptativo()
    results = adaptador.run([])

    assert results["status"] == "no_evaluation_results"
    assert results["num_hard_negatives"] == 0
    assert len(results["hard_negatives_identified"]) == 0
    mock_trigger_fine_tuning.assert_not_called() # No fine-tuning if no input

def test_identify_hard_negatives_missing_keys():
    """
    Test _identify_hard_negatives with items missing expected keys.
    """
    adaptador = RetrieverAdaptativo(negative_mining_threshold=0.5)
    
    # Missing 'avaliacao_automatica' and 'avaliacao_llm_judge'
    results_missing_eval = [
        {"query": "Query A", "answer": "Answer A", "context_documents": ["Doc A"]},
        {"query": "Query B", "answer": "Não sei.", "context_documents": ["Doc B"]}, # Should be hard negative due to answer
    ]
    hard_negatives = adaptador._identify_hard_negatives(results_missing_eval)
    assert len(hard_negatives) == 1
    assert hard_negatives[0]["query"] == "Query B"

@patch('src.O.retriever_adaptativo.retriever_adaptativo.logger.warning')
def test_trigger_fine_tuning_with_hard_negatives(mock_logger_warning):
    """
    Test _trigger_fine_tuning when hard negatives are present.
    """
    adaptador = RetrieverAdaptativo()
    hard_negatives = [{"query": "HN1"}, {"query": "HN2"}]
    adaptador._trigger_fine_tuning(hard_negatives)
    mock_logger_warning.assert_called_once_with("Processo de fine-tuning do retriever disparado com 2 hard negatives.")

@patch('src.O.retriever_adaptativo.retriever_adaptativo.logger.info')
def test_trigger_fine_tuning_no_hard_negatives(mock_logger_info):
    """
    Test _trigger_fine_tuning when no hard negatives are present.
    """
    adaptador = RetrieverAdaptativo()
    adaptador._trigger_fine_tuning([])
    mock_logger_info.assert_called_once_with("Nenhum hard negative identificado. Fine-tuning não disparado.")