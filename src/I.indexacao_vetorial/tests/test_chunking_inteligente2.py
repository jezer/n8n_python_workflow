import pytest
from unittest.mock import MagicMock, patch, mock_open, call
import numpy as np
import os
import json

# Assume the class is in src.I.indexacao_vetorial.indexacao_vetorial
# Adjust if the actual path or class name differs.
from src.I.indexacao_vetorial.indexacao_vetorial import IndexacaoVetorial

MOCK_INDEX_BASE_PATH = "./test_indices"
MOCK_EMBEDDING_DIM = 5

@pytest.fixture
def mock_data_with_embeddings():
    return [
        {"embedding": np.array([1.0, 1.1, 1.2, 1.3, 1.4]), "referencia": "doc1_q1"},
        {"embedding": np.array([2.0, 2.1, 2.2, 2.3, 2.4]), "referencia": "doc2_q1"},
        {"embedding": [3.0, 3.1, 3.2, 3.3, 3.4], "referencia": "doc3_q1"}, # list type
    ]

@pytest.fixture
def mock_data_invalid_embeddings():
    return [
        {"embedding": np.array([1.0, 1.1]), "referencia": "short_emb"}, # wrong dim
        {"embedding": "not an embedding", "referencia": "invalid_type"},
        {"referencia": "no_embedding_key"},
        {"embedding": [], "referencia": "empty_list_emb"},
    ]

@pytest.fixture(autouse=True)
def cleanup_test_indices():
    """Ensure the test index directory is clean before and after tests if created."""
    if os.path.exists(MOCK_INDEX_BASE_PATH):
        for f in os.listdir(MOCK_INDEX_BASE_PATH):
            os.remove(os.path.join(MOCK_INDEX_BASE_PATH, f))
        # os.rmdir(MOCK_INDEX_BASE_PATH) # Keep if tests create it
    yield
    if os.path.exists(MOCK_INDEX_BASE_PATH):
        for f in os.listdir(MOCK_INDEX_BASE_PATH):
            os.remove(os.path.join(MOCK_INDEX_BASE_PATH, f))
        # os.rmdir(MOCK_INDEX_BASE_PATH)


class TestIndexacaoVetorial:

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.os.makedirs')
    def test_init_creates_directory(self, mock_makedirs):
        """Test if __init__ attempts to create the base directory."""
        IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        mock_makedirs.assert_called_once_with(MOCK_INDEX_BASE_PATH, exist_ok=True)

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.faiss')
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.os.path.exists', return_value=False) # For save
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.json.dump')
    def test_run_happy_path(self, mock_json_dump, mock_file_open, mock_os_exists, mock_faiss_module, mock_data_with_embeddings):
        """Test the run method with valid embeddings."""
        mock_index_instance = MagicMock()
        mock_faiss_module.IndexFlatL2.return_value = mock_index_instance
        # mock_faiss_module.IndexHNSWFlat.return_value = mock_index_instance # If using HNSW

        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        versao = "test001"
        indexer.run(mock_data_with_embeddings, versao)

        mock_faiss_module.IndexFlatL2.assert_called_once_with(MOCK_EMBEDDING_DIM)
        # mock_faiss_module.IndexHNSWFlat.assert_called_once_with(MOCK_EMBEDDING_DIM, 32)

        # Check if embeddings were added
        assert mock_index_instance.add.call_count == 1
        added_embeddings = mock_index_instance.add.call_args[0][0]
        assert isinstance(added_embeddings, np.ndarray)
        assert added_embeddings.shape == (len(mock_data_with_embeddings), MOCK_EMBEDDING_DIM)
        assert added_embeddings.dtype == np.float32

        # Check if index was written
        expected_index_path = os.path.join(MOCK_INDEX_BASE_PATH, f"index_v{versao}.faiss")
        mock_faiss_module.write_index.assert_called_once_with(mock_index_instance, expected_index_path)

        # Check if metadata was saved
        expected_metadata_path = os.path.join(MOCK_INDEX_BASE_PATH, f"index_v{versao}_meta.json")
        mock_file_open.assert_called_once_with(expected_metadata_path, 'w')
        expected_metadata = [item['referencia'] for item in mock_data_with_embeddings]
        mock_json_dump.assert_called_once_with(expected_metadata, mock_file_open())

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.faiss')
    def test_run_empty_input_data(self, mock_faiss_module):
        """Test run with an empty list of embeddings."""
        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        indexer.run([], "test002")
        mock_faiss_module.IndexFlatL2.assert_not_called()
        mock_faiss_module.write_index.assert_not_called()

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.faiss')
    def test_run_no_valid_embeddings_in_data(self, mock_faiss_module, mock_data_invalid_embeddings):
        """Test run when data contains no processable embeddings."""
        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        # Filter out the "wrong_dim" case for this specific test if it would cause vstack to fail early
        # or ensure the hypothetical code handles it before vstack.
        # For this test, assume the code filters them out before `IndexFlatL2` or `add`.
        data_that_will_be_empty = [
            d for d in mock_data_invalid_embeddings if not isinstance(d.get("embedding"), np.ndarray) or d.get("embedding").ndim !=1
        ]
        if not any(isinstance(d.get("embedding"), np.ndarray) and d.get("embedding").size == MOCK_EMBEDDING_DIM for d in mock_data_invalid_embeddings):
             indexer.run(mock_data_invalid_embeddings, "test003")
             mock_faiss_module.IndexFlatL2.assert_not_called()
             mock_faiss_module.write_index.assert_not_called()
        else:
            # This case implies some embeddings might be valid, adjust test if needed
            pass

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.faiss.read_index')
    @patch('builtins.open', new_callable=mock_open, read_data='["meta1", "meta2"]')
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.os.path.exists', return_value=True)
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.json.load')
    def test_load_index_success(self, mock_json_load, mock_os_exists, mock_file_open, mock_read_index):
        """Test successfully loading an existing index."""
        mock_faiss_index = MagicMock()
        mock_faiss_index.ntotal = 2
        mock_read_index.return_value = mock_faiss_index
        mock_json_load.return_value = ["meta1", "meta2"]

        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        versao = "test004"
        loaded = indexer.load_index(versao)

        assert loaded is True
        assert indexer.index == mock_faiss_index
        assert indexer.metadata == ["meta1", "meta2"]
        expected_index_path = os.path.join(MOCK_INDEX_BASE_PATH, f"index_v{versao}.faiss")
        mock_read_index.assert_called_once_with(expected_index_path)
        expected_metadata_path = os.path.join(MOCK_INDEX_BASE_PATH, f"index_v{versao}_meta.json")
        mock_file_open.assert_called_once_with(expected_metadata_path, 'r')
        mock_json_load.assert_called_once_with(mock_file_open())

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.os.path.exists', return_value=False)
    def test_load_index_not_found(self, mock_os_exists):
        """Test loading when index files do not exist."""
        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        versao = "nonexistent_v001"
        loaded = indexer.load_index(versao)
        
        assert loaded is False
        assert indexer.index is None
        # Check that os.path.exists was called for both index and metadata
        expected_index_path = os.path.join(MOCK_INDEX_BASE_PATH, f"index_v{versao}.faiss")
        # expected_metadata_path = os.path.join(MOCK_INDEX_BASE_PATH, f"index_v{versao}_meta.json")
        # mock_os_exists.assert_any_call(expected_index_path)
        # mock_os_exists.assert_any_call(expected_metadata_path) # Exact calls depend on implementation logic
        assert mock_os_exists.call_count >= 1 # At least index path checked

    def test_search_no_index(self):
        """Test search when no index is loaded/built."""
        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        query_emb = np.random.rand(1, MOCK_EMBEDDING_DIM).astype(np.float32)
        results = indexer.search(query_emb, k=3)
        assert results == []

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.faiss.read_index')
    @patch('builtins.open', new_callable=mock_open, read_data='["ref1", "ref2", "ref3"]')
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.os.path.exists', return_value=True)
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.json.load')
    def test_search_with_loaded_index(self, mock_json_load, mock_os_exists, mock_file_open, mock_read_index):
        """Test search functionality with a mocked loaded index."""
        mock_faiss_index = MagicMock()
        # D: distances, I: indices
        mock_distances = np.array([[0.1, 0.2, 0.3]], dtype=np.float32)
        mock_indices = np.array([[0, 2, 1]], dtype=np.int64) # Indices into metadata
        mock_faiss_index.search.return_value = (mock_distances, mock_indices)
        mock_read_index.return_value = mock_faiss_index
        
        mock_metadata = ["Referencia A", "Referencia B", "Referencia C"]
        mock_json_load.return_value = mock_metadata

        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        indexer.load_index("search_test_v001") # Load the mocked index and metadata
        
        assert indexer.index is not None # Ensure index is loaded
        assert indexer.metadata == mock_metadata

        query_emb = np.random.rand(MOCK_EMBEDDING_DIM).astype(np.float32) # 1D query
        k = 3
        results = indexer.search(query_emb, k=k)

        mock_faiss_index.search.assert_called_once()
        # Check the query embedding passed to faiss_index.search
        search_args = mock_faiss_index.search.call_args[0]
        assert search_args[0].shape == (1, MOCK_EMBEDDING_DIM) # Should be 2D for FAISS
        assert search_args[1] == k

        assert len(results) == k
        assert results[0] == {"referencia": mock_metadata[0], "distancia": 0.1, "indice_original": 0}
        assert results[1] == {"referencia": mock_metadata[2], "distancia": 0.2, "indice_original": 2}
        assert results[2] == {"referencia": mock_metadata[1], "distancia": 0.3, "indice_original": 1}

    @patch('src.I.indexacao_vetorial.indexacao_vetorial.faiss')
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.I.indexacao_vetorial.indexacao_vetorial.json.dump')
    def test_run_handles_vstack_error_gracefully(self, mock_json_dump, mock_file_open, mock_os_exists, mock_faiss_module, capsys):
        """Test that run handles ValueError from np.vstack (e.g., inconsistent embedding dimensions)"""
        # This requires the hypothetical IndexacaoVetorial to have try-except around np.vstack
        mock_data_inconsistent_dim = [
            {"embedding": np.array([1.0, 1.1, 1.2, 1.3, 1.4]), "referencia": "doc1_q1"},
            {"embedding": np.array([2.0, 2.1, 2.2]), "referencia": "doc2_q1_short"}, # Different dimension
        ]
        
        indexer = IndexacaoVetorial(index_base_path=MOCK_INDEX_BASE_PATH)
        versao = "vstack_fail"
        
        # Assuming the run method prints an error and doesn't build an index
        indexer.run(mock_data_inconsistent_dim, versao)
        
        captured = capsys.readouterr()
        assert "Error stacking embeddings" in captured.out # Check for a log/print message
        mock_faiss_module.IndexFlatL2.assert_not_called()
        mock_faiss_module.write_index.assert_not_called()
        mock_json_dump.assert_not_called()

```

This test suite covers:
*   Initialization of `IndexacaoVetorial`.
*   The `run` method for happy path, empty input, and input with no valid embeddings. It also checks for graceful handling of `np.vstack` errors if embeddings have inconsistent dimensions (this assumes the `IndexacaoVetorial` implementation has such error handling).
*   `load_index` for success and file-not-found scenarios.
*   `search` method when an index is loaded and when no index is present.
*   Mocking of `faiss`, `os` operations, and `json` operations to isolate the class logic.
*   Use of fixtures for test data.
*   A cleanup fixture to manage test artifacts if the `IndexacaoVetorial` class actually creates files (though mocks prevent this in most tests here).

To make these tests fully align, the actual `indexacao_vetorial.py` would be needed. The current tests are based on a reasonable hypothetical implementation derived from the provided context.

<!--
[PROMPT_SUGGESTION]Refactor the `IndexacaoVetorial` class to inject the FAISS index object for more granular testing of its interaction with FAISS.[/PROMPT_SUGGESTION]
[PROMPT_SUGGESTION]Add tests for different FAISS index types (e.g., IndexHNSWFlat) if the `IndexacaoVetorial` class supports configuring them.[/PROMPT_SUGGESTION]
->
