import pytest
from unittest.mock import MagicMock, patch
import numpy as np

# Assuming the class is in src.H.embeddings_especializados.embeddings_especializados
# Adjust the import path if the file/class name is different.
from src.H.embeddings_especializados.embeddings_especializados import EmbeddingsEspecializados

MOCK_MODEL_NAME = 'mock-instructor-xl'
MOCK_EMBEDDING_DIM = 10 # Simplified dimension for mock embeddings

@pytest.fixture
def mock_qa_data_valid():
    return [
        {"pergunta_gerada": "Qual a capital da França?", "resposta_gerada": "Paris"},
        {"pergunta_gerada": "Quem escreveu Dom Quixote?", "resposta_gerada": "Miguel de Cervantes"},
    ]

@pytest.fixture
def mock_qa_data_mixed():
    return [
        {"pergunta_gerada": "Qual a cor do céu?", "resposta_gerada": "Azul"}, # Valid
        {"pergunta_gerada": "E sobre a lua?", "resposta_gerada": ""},          # Resposta vazia
        {"pergunta_gerada": "", "resposta_gerada": "Apenas uma resposta."},    # Pergunta vazia
        {"pergunta_gerada": "", "resposta_gerada": ""},                       # Ambos vazios
        {"outro_campo": "valor"},                                            # Sem P nem R
    ]

@patch('src.H.embeddings_especializados.embeddings_especializados.SentenceTransformer')
def test_embeddings_especializados_init_success(mock_sentence_transformer_class):
    """Test successful initialization and model loading."""
    mock_model_instance = MagicMock()
    mock_sentence_transformer_class.return_value = mock_model_instance
    
    handler = EmbeddingsEspecializados(model_name=MOCK_MODEL_NAME)
    
    mock_sentence_transformer_class.assert_called_once_with(MOCK_MODEL_NAME)
    assert handler.model == mock_model_instance
    assert handler.model_name == MOCK_MODEL_NAME

@patch('src.H.embeddings_especializados.embeddings_especializados.SentenceTransformer')
def test_embeddings_especializados_init_model_load_failure(mock_sentence_transformer_class):
    """Test initialization when model loading fails."""
    mock_sentence_transformer_class.side_effect = Exception("Model load error")
    
    # Assuming the constructor handles this by setting self.model to None or similar
    # and does not raise the exception itself, or if it does, we can test for that.
    # For this example, let's assume it logs and sets model to None.
    # This behavior depends on the actual implementation of __init__.
    with pytest.warns(UserWarning, match="Error loading model mock-fail-model: Model load error"): # Or check logs
        handler = EmbeddingsEspecializados(model_name='mock-fail-model')
    
    assert handler.model is None
    mock_sentence_transformer_class.assert_called_once_with('mock-fail-model')

@patch('src.H.embeddings_especializados.embeddings_especializados.SentenceTransformer')
def test_run_happy_path(mock_sentence_transformer_class, mock_qa_data_valid):
    """Test the run method with valid QA data."""
    mock_model_instance = MagicMock()
    # Mock the encode method to return predictable embeddings
    mock_embeddings = [np.array([i]*MOCK_EMBEDDING_DIM) for i in range(len(mock_qa_data_valid))]
    mock_model_instance.encode.return_value = mock_embeddings
    mock_sentence_transformer_class.return_value = mock_model_instance

    handler = EmbeddingsEspecializados(model_name=MOCK_MODEL_NAME)
    resultados = handler.run(mock_qa_data_valid)

    assert len(resultados) == len(mock_qa_data_valid)
    expected_texts_to_encode = []
    for i, item in enumerate(mock_qa_data_valid):
        assert "embedding" in resultados[i]
        assert isinstance(resultados[i]["embedding"], np.ndarray)
        assert resultados[i]["embedding"].shape == (MOCK_EMBEDDING_DIM,)
        np.testing.assert_array_equal(resultados[i]["embedding"], mock_embeddings[i])
        
        # Construct expected text for embedding based on assumed _prepare_text_for_embedding logic
        pergunta = item.get("pergunta_gerada", "")
        resposta = item.get("resposta_gerada", "")
        expected_text = f"Pergunta: {pergunta} Resposta: {resposta}"
        expected_texts_to_encode.append(expected_text)
        
        # Verify referencia (assuming it's the pergunta if available)
        assert resultados[i]["referencia"] == pergunta

    mock_model_instance.encode.assert_called_once_with(expected_texts_to_encode)

@patch('src.H.embeddings_especializados.embeddings_especializados.SentenceTransformer')
def test_run_empty_input(mock_sentence_transformer_class):
    """Test the run method with an empty list of QA data."""
    mock_model_instance = MagicMock()
    mock_sentence_transformer_class.return_value = mock_model_instance
    
    handler = EmbeddingsEspecializados(model_name=MOCK_MODEL_NAME)
    resultados = handler.run([])
    
    assert resultados == []
    mock_model_instance.encode.assert_not_called()

@patch('src.H.embeddings_especializados.embeddings_especializados.SentenceTransformer')
def test_run_with_mixed_qa_data(mock_sentence_transformer_class, mock_qa_data_mixed):
    """Test run with mixed QA data (valid, missing parts, empty parts)."""
    mock_model_instance = MagicMock()
    
    # Define side effect for encode based on input text
    def mock_encode_side_effect(texts_to_encode):
        embeddings = []
        for text in texts_to_encode:
            if "Qual a cor do céu?" in text:
                embeddings.append(np.array([1.0]*MOCK_EMBEDDING_DIM))
            elif "E sobre a lua?" in text: # Only P
                embeddings.append(np.array([2.0]*MOCK_EMBEDDING_DIM))
            elif "Apenas uma resposta." in text: # Only R
                embeddings.append(np.array([3.0]*MOCK_EMBEDDING_DIM))
            else: # Should not happen if prepare_text filters empty
                embeddings.append(np.array([0.0]*MOCK_EMBEDDING_DIM))
        return embeddings
        
    mock_model_instance.encode.side_effect = mock_encode_side_effect
    mock_sentence_transformer_class.return_value = mock_model_instance

    handler = EmbeddingsEspecializados(model_name=MOCK_MODEL_NAME)
    resultados = handler.run(mock_qa_data_mixed)

    assert len(resultados) == len(mock_qa_data_mixed)

    # Item 0: Valid P & R
    assert "embedding" in resultados[0] and isinstance(resultados[0]["embedding"], np.ndarray)
    np.testing.assert_array_equal(resultados[0]["embedding"], np.array([1.0]*MOCK_EMBEDDING_DIM))
    assert resultados[0]["referencia"] == "Qual a cor do céu?"

    # Item 1: Valid P, Empty R
    assert "embedding" in resultados[1] and isinstance(resultados[1]["embedding"], np.ndarray)
    np.testing.assert_array_equal(resultados[1]["embedding"], np.array([2.0]*MOCK_EMBEDDING_DIM))
    assert resultados[1]["referencia"] == "E sobre a lua?"

    # Item 2: Empty P, Valid R
    assert "embedding" in resultados[2] and isinstance(resultados[2]["embedding"], np.ndarray)
    np.testing.assert_array_equal(resultados[2]["embedding"], np.array([3.0]*MOCK_EMBEDDING_DIM))
    assert resultados[2]["referencia"] == "Apenas uma resposta." # Assuming reference is R if P is empty

    # Item 3: Empty P & R (assuming _prepare_text_for_embedding returns empty text, leading to no embedding or specific handling)
    # Behavior depends on how EmbeddingsEspecializados handles items that yield no text_to_embed.
    # Assuming it results in an empty np.array([]) for embedding and "N/A" for referencia.
    assert "embedding" in resultados[3]
    assert resultados[3]["embedding"].size == 0 # Or check for a specific error marker
    assert resultados[3]["referencia"] == "N/A"

    # Item 4: No P nor R keys
    assert "embedding" in resultados[4]
    assert resultados[4]["embedding"].size == 0 # Or check for a specific error marker
    assert resultados[4]["referencia"] == "N/A"
    
    # Check texts passed to encode
    actual_encoded_texts = mock_model_instance.encode.call_args[0][0]
    assert len(actual_encoded_texts) == 3 # Only 3 items should have produced non-empty text
    assert "Pergunta: Qual a cor do céu? Resposta: Azul" in actual_encoded_texts
    assert "E sobre a lua?" in actual_encoded_texts # Assuming P only becomes the text
    assert "Apenas uma resposta." in actual_encoded_texts # Assuming R only becomes the text

@patch('src.H.embeddings_especializados.embeddings_especializados.SentenceTransformer')
def test_run_model_not_loaded(mock_sentence_transformer_class, mock_qa_data_valid):
    """Test run method when the model failed to load during __init__."""
    mock_sentence_transformer_class.side_effect = Exception("Model load error")
    
    with pytest.warns(UserWarning): # Suppress warning during init
        handler = EmbeddingsEspecializados(model_name='mock-fail-model')
    assert handler.model is None

    resultados = handler.run(mock_qa_data_valid)
    
    # Behavior depends on implementation:
    # Option 1: Raises an error
    # with pytest.raises(RuntimeError, match="Embedding model is not loaded."):
    # handler.run(mock_qa_data_valid)
    # Option 2: Returns items with an error field (as assumed in hypothetical code)
    assert len(resultados) == len(mock_qa_data_valid)
    for item in resultados:
        assert item.get("error_embedding") == "Embedding model is not loaded." # Or similar error indicator
        assert "embedding" not in item or item["embedding"].size == 0

@patch('src.H.embeddings_especializados.embeddings_especializados.SentenceTransformer')
def test_run_model_encode_fails_for_item(mock_sentence_transformer_class, mock_qa_data_valid):
    """Test when model.encode() raises an exception for a specific item."""
    mock_model_instance = MagicMock()
    mock_model_instance.encode.side_effect = Exception("Encoding failed for this item")
    mock_sentence_transformer_class.return_value = mock_model_instance

    handler = EmbeddingsEspecializados(model_name=MOCK_MODEL_NAME)
    resultados = handler.run(mock_qa_data_valid)

    assert len(resultados) == len(mock_qa_data_valid)
    for i, item in enumerate(resultados):
        assert item.get("error_embedding") == "Encoding failed for this item"
        assert "embedding" not in item or item["embedding"].size == 0