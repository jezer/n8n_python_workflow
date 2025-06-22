import pytest
from unittest.mock import MagicMock, patch, call
import numpy as np

# Assume the class is in src.L.reranking_cross_encoder.reranking_cross_encoder
# Adjust the import path if the file/class name is different.
from src.L.reranking_cross_encoder.reranking_cross_encoder import RerankingCrossEncoder

# --- Fixtures for Mock Data and Dependencies ---

@pytest.fixture
def mock_retriever_results_valid():
    """
    Simulates input from the HybridRetriever step.
    Each 'resultado' item includes 'document', 'score', and 'idx'.
    """
    return [
        {
            "query": "inteligência artificial",
            "resultados": [
                {"document": "Este é o documento um sobre inteligência artificial e aprendizado de máquina.", "score": 0.8, "idx": 0},
                {"document": "Quarto documento é sobre ciência de dados e estatística.", "score": 0.5, "idx": 3},
                {"document": "Documento dois fala sobre redes neurais e deep learning.", "score": 0.3, "idx": 1},
            ]
        },
        {
            "query": "redes neurais",
            "resultados": [
                {"document": "Documento dois fala sobre redes neurais e deep learning.", "score": 0.7, "idx": 1},
                {"document": "Terceiro documento aborda processamento de linguagem natural e BERT.", "score": 0.4, "idx": 2},
            ]
        }
    ]

@pytest.fixture
def mock_cross_encoder_model():
    """Mocks the CrossEncoder model's predict method."""
    mock_encoder = MagicMock()
    
    def predict_side_effect(pairs):
        # Simulate scores for specific query-document pairs
        scores = []
        for query, doc_text in pairs:
            if "inteligência artificial" in query:
                if "documento um" in doc_text: scores.append(0.95) # Highly relevant
                elif "ciência de dados" in doc_text: scores.append(0.60) # Moderately relevant
                elif "redes neurais" in doc_text: scores.append(0.10) # Not very relevant
                else: scores.append(0.0)
            elif "redes neurais" in query:
                if "Documento dois" in doc_text: scores.append(0.85) # Highly relevant
                elif "processamento de linguagem" in doc_text: scores.append(0.40) # Less relevant
                else: scores.append(0.0)
            else:
                scores.append(0.0) # Default for unmocked pairs
        return np.array(scores)

    mock_encoder.predict.side_effect = predict_side_effect
    return mock_encoder

# --- Tests for RerankingCrossEncoder ---

@patch('src.L.reranking_cross_encoder.reranking_cross_encoder.CrossEncoder')
def test_reranker_init_success(mock_cross_encoder_class, mock_cross_encoder_model):
    """Test successful initialization and model loading."""
    mock_cross_encoder_class.return_value = mock_cross_encoder_model
    
    reranker = RerankingCrossEncoder(model_name="test-model")
    
    mock_cross_encoder_class.assert_called_once_with("test-model")
    assert reranker.reranker == mock_cross_encoder_model

@patch('src.L.reranking_cross_encoder.reranking_cross_encoder.CrossEncoder')
def test_reranker_init_model_load_failure(mock_cross_encoder_class):
    """Test initialization when model loading fails."""
    mock_cross_encoder_class.side_effect = Exception("Model load error")
    
    reranker = RerankingCrossEncoder(model_name="mock-fail-model")
    
    assert reranker.reranker is None
    mock_cross_encoder_class.assert_called_once_with("mock-fail-model")

@patch('src.L.reranking_cross_encoder.reranking_cross_encoder.CrossEncoder')
def test_run_happy_path(mock_cross_encoder_class, mock_cross_encoder_model, mock_retriever_results_valid):
    """
    Test successful reranking for multiple queries with multiple documents.
    """
    mock_cross_encoder_class.return_value = mock_cross_encoder_model
    reranker = RerankingCrossEncoder()

    results = reranker.run(mock_retriever_results_valid)

    assert len(results) == len(mock_retriever_results_valid)
    mock_cross_encoder_model.predict.call_count == len(mock_retriever_results_valid)

    # Verify reranking for the first query
    query1_results = results[0]["resultados"]
    assert len(query1_results) == 3
    assert query1_results[0]["document"] == "Este é o documento um sobre inteligência artificial e aprendizado de máquina."
    assert query1_results[0]["score"] == 0.95
    assert query1_results[1]["document"] == "Quarto documento é sobre ciência de dados e estatística."
    assert query1_results[1]["score"] == 0.60
    assert query1_results[2]["document"] == "Documento dois fala sobre redes neurais e deep learning."
    assert query1_results[2]["score"] == 0.10

    # Verify reranking for the second query
    query2_results = results[1]["resultados"]
    assert len(query2_results) == 2
    assert query2_results[0]["document"] == "Documento dois fala sobre redes neurais e deep learning."
    assert query2_results[0]["score"] == 0.85
    assert query2_results[1]["document"] == "Terceiro documento aborda processamento de linguagem natural e BERT."
    assert query2_results[1]["score"] == 0.40

@patch('src.L.reranking_cross_encoder.reranking_cross_encoder.CrossEncoder')
def test_run_empty_input(mock_cross_encoder_class):
    """Test run with an empty list of retrieval results."""
    mock_cross_encoder_class.return_value = MagicMock()
    reranker = RerankingCrossEncoder()
    results = reranker.run([])
    assert results == []
    mock_cross_encoder_class.return_value.predict.assert_not_called()

@patch('src.L.reranking_cross_encoder.reranking_cross_encoder.CrossEncoder')
def test_run_query_with_no_results(mock_cross_encoder_class):
    """Test run with a query that has an empty 'resultados' list."""
    mock_cross_encoder_class.return_value = MagicMock()
    reranker = RerankingCrossEncoder()
    input_data = [{"query": "empty query", "resultados": []}]
    results = reranker.run(input_data)
    assert results == input_data # Should return original data
    mock_cross_encoder_class.return_value.predict.assert_not_called()

@patch('src.L.reranking_cross_encoder.reranking_cross_encoder.CrossEncoder')
def test_run_predict_failure(mock_cross_encoder_class, mock_retriever_results_valid):
    """
    Test that if predict fails for a query, its original results are returned,
    and other queries are still processed.
    """
    mock_cross_encoder_instance = MagicMock()
    mock_cross_encoder_class.return_value = mock_cross_encoder_instance
    
    # Simulate predict failing for the first query, but working for the second
    mock_cross_encoder_instance.predict.side_effect = [
        Exception("Cross-encoder prediction failed"), # For first query
        np.array([0.85, 0.40]) # For second query
    ]

    reranker = RerankingCrossEncoder()
    results = reranker.run(mock_retriever_results_valid)

    assert len(results) == len(mock_retriever_results_valid)
    # First query should return original results due to error
    assert results[0] == mock_retriever_results_valid[0]
    # Second query should be reranked successfully
    assert results[1]["resultados"][0]["score"] == 0.85
    assert results[1]["resultados"][1]["score"] == 0.40

@patch('src.L.reranking_cross_encoder.reranking_cross_encoder.CrossEncoder')
def test_run_model_not_loaded(mock_cross_encoder_class, mock_retriever_results_valid):
    """Test run method when the CrossEncoder model failed to load during __init__."""
    mock_cross_encoder_class.side_effect = Exception("Model load error") # Simulate init failure
    reranker = RerankingCrossEncoder() # This will result in self.reranker being None
    
    assert reranker.reranker is None
    
    results = reranker.run(mock_retriever_results_valid)
    
    # Should return original results if model is not loaded
    assert results == mock_retriever_results_valid
    mock_cross_encoder_class.return_value.predict.assert_not_called() # Ensure predict was never called

# Add more test cases as needed:
# - Test with a single document per query.
# - Test with documents that have identical scores from the cross-encoder.
# - Test the preservation of 'idx' and 'original_score' fields.