import pytest
from unittest.mock import MagicMock, patch, call
import numpy as np

# Assume the class is in src.K.hybrid_retriever.hybrid_retriever
# Adjust the import path if the file/class name is different.
from src.K.hybrid_retriever.hybrid_retriever import HybridRetriever

# --- Fixtures for Mock Data and Dependencies ---

@pytest.fixture
def mock_documents():
    return [
        "Este é o documento um sobre inteligência artificial e aprendizado de máquina.",
        "Documento dois fala sobre redes neurais e deep learning.",
        "Terceiro documento aborda processamento de linguagem natural e BERT.",
        "Quarto documento é sobre ciência de dados e estatística.",
        "Documento cinco é um texto genérico sem termos específicos."
    ]

@pytest.fixture
def mock_queries():
    return [
        "inteligência artificial",
        "redes neurais",
        "processamento de linguagem"
    ]

@pytest.fixture
def mock_sentence_transformer():
    """Mocks the SentenceTransformer model."""
    mock_model = MagicMock()
    # Simulate embeddings for documents and queries
    # For simplicity, let's make them distinct but somewhat related for testing
    def encode_side_effect(texts, convert_to_tensor=False):
        embeddings = []
        for text in texts:
            if "inteligência artificial" in text:
                embeddings.append(np.array([0.9, 0.1, 0.1]))
            elif "redes neurais" in text:
                embeddings.append(np.array([0.1, 0.9, 0.1]))
            elif "processamento de linguagem" in text:
                embeddings.append(np.array([0.1, 0.1, 0.9]))
            elif "documento um" in text:
                embeddings.append(np.array([0.85, 0.15, 0.1]))
            elif "documento dois" in text:
                embeddings.append(np.array([0.15, 0.85, 0.1]))
            elif "Terceiro documento" in text:
                embeddings.append(np.array([0.1, 0.15, 0.85]))
            else:
                embeddings.append(np.array([0.5, 0.5, 0.5])) # Generic embedding
        return np.array(embeddings)

    mock_model.encode.side_effect = encode_side_effect
    return mock_model

@pytest.fixture
def mock_faiss_index():
    """Mocks a FAISS index."""
    mock_index = MagicMock()
    # Simulate search results (distances, indices)
    # For a query, return relevant documents with low distance
    def search_side_effect(query_embedding, k):
        # Simple logic: if query_embedding is close to doc_embedding, return it
        # This needs to be aligned with mock_sentence_transformer's output
        if np.allclose(query_embedding, np.array([[0.9, 0.1, 0.1]])): # Query: IA
            return np.array([[0.05, 0.15]]), np.array([[0, 3]]) # Doc 0, Doc 3
        elif np.allclose(query_embedding, np.array([[0.1, 0.9, 0.1]])): # Query: Redes Neurais
            return np.array([[0.05, 0.15]]), np.array([[1, 4]]) # Doc 1, Doc 4
        elif np.allclose(query_embedding, np.array([[0.1, 0.1, 0.9]])): # Query: PLN
            return np.array([[0.05, 0.15]]), np.array([[2, 0]]) # Doc 2, Doc 0
        return np.array([[]]), np.array([[]]) # No results

    mock_index.search.side_effect = search_side_effect
    return mock_index

@pytest.fixture
def mock_bm25_model():
    """Mocks a BM25 model."""
    mock_bm25 = MagicMock()
    # Simulate BM25 scores (doc_idx, score)
    def get_top_n_side_effect(query, documents, n):
        results = []
        if "inteligência artificial" in query:
            results.append((0, 0.8)) # Doc 0 is highly relevant
            results.append((3, 0.5)) # Doc 3 is somewhat relevant
        elif "redes neurais" in query:
            results.append((1, 0.8)) # Doc 1 is highly relevant
            results.append((4, 0.5)) # Doc 4 is somewhat relevant
        elif "processamento de linguagem" in query:
            results.append((2, 0.8)) # Doc 2 is highly relevant
            results.append((0, 0.5)) # Doc 0 is somewhat relevant
        return results[:n]

    mock_bm25.get_top_n.side_effect = get_top_n_side_effect
    return mock_bm25

@pytest.fixture
def mock_cache():
    """Mocks a cache object (e.g., from cachetools)."""
    mock_cache_instance = MagicMock()
    mock_cache_instance.__contains__.return_value = False # Default: no cache hit
    mock_cache_instance.__getitem__.side_effect = KeyError # Default: no cache hit
    mock_cache_instance.__setitem__.return_value = None
    return mock_cache_instance

# --- Tests for HybridRetriever ---

@patch('src.K.hybrid_retriever.hybrid_retriever.SentenceTransformer')
@patch('src.K.hybrid_retriever.hybrid_retriever.faiss')
@patch('src.K.hybrid_retriever.hybrid_retriever.BM25Okapi')
@patch('src.K.hybrid_retriever.hybrid_retriever.TTLCache')
def test_hybrid_retriever_init(mock_ttl_cache, mock_bm25_okapi, mock_faiss, mock_sentence_transformer):
    """Test initialization of HybridRetriever."""
    retriever = HybridRetriever(
        dense_model_name="test-model",
        bm25_tokenizer=None, # Mocked away
        faiss_index_path="test-index.faiss",
        cache_ttl=3600
    )
    mock_sentence_transformer.assert_called_once_with("test-model")
    mock_faiss.read_index.assert_called_once_with("test-index.faiss")
    mock_ttl_cache.assert_called_once_with(maxsize=1000, ttl=3600)
    assert retriever.dense_weight == 0.6
    assert retriever.sparse_weight == 0.4

@patch('src.K.hybrid_retriever.hybrid_retriever.SentenceTransformer')
@patch('src.K.hybrid_retriever.hybrid_retriever.faiss')
@patch('src.K.hybrid_retriever.hybrid_retriever.BM25Okapi')
@patch('src.K.hybrid_retriever.hybrid_retriever.TTLCache')
def test_retrieve_happy_path(mock_ttl_cache, mock_bm25_okapi, mock_faiss, mock_sentence_transformer,
                             mock_documents, mock_queries, mock_bm25_model, mock_faiss_index, mock_sentence_transformer):
    """
    Test successful hybrid retrieval with both dense and sparse components.
    """
    # Configure mocks
    mock_sentence_transformer.return_value = mock_sentence_transformer # Use the fixture's mock
    mock_faiss.read_index.return_value = mock_faiss_index
    mock_bm25_okapi.return_value = mock_bm25_model
    mock_ttl_cache.return_value = mock_cache # Use the fixture's mock

    retriever = HybridRetriever(
        dense_model_name="test-model",
        bm25_tokenizer=lambda x: x.split(), # Simple tokenizer for BM25 mock
        faiss_index_path="test-index.faiss",
        cache_ttl=3600
    )

    query = mock_queries[0] # "inteligência artificial"
    k = 2
    results = retriever.retrieve(query, mock_documents, k=k)

    # Assertions
    mock_sentence_transformer.encode.assert_called_with([query]) # Query embedding
    mock_faiss_index.search.assert_called_once() # Dense search
    mock_bm25_model.get_top_n.assert_called_once() # Sparse search

    assert len(results) == k
    assert "document" in results[0]
    assert "score" in results[0]
    assert results[0]["document"] == mock_documents[0] # Doc 0 should be top
    assert results[1]["document"] == mock_documents[3] # Doc 3 should be second

    # Verify scores (rough check, exact values depend on mock BM25/FAISS scores)
    # Dense score for doc 0: 1.0 - 0.05 = 0.95
    # Sparse score for doc 0: 0.8
    # Combined score for doc 0: 0.95 * 0.6 + 0.8 * 0.4 = 0.57 + 0.32 = 0.89
    # Dense score for doc 3: 1.0 - 0.15 = 0.85
    # Sparse score for doc 3: 0.5
    # Combined score for doc 3: 0.85 * 0.6 + 0.5 * 0.4 = 0.51 + 0.2 = 0.71
    assert results[0]["score"] > results[1]["score"]

@patch('src.K.hybrid_retriever.hybrid_retriever.SentenceTransformer')
@patch('src.K.hybrid_retriever.hybrid_retriever.faiss')
@patch('src.K.hybrid_retriever.hybrid_retriever.BM25Okapi')
@patch('src.K.hybrid_retriever.hybrid_retriever.TTLCache')
def test_retrieve_dense_fallback_to_sparse(mock_ttl_cache, mock_bm25_okapi, mock_faiss, mock_sentence_transformer,
                                         mock_documents, mock_queries, mock_bm25_model, mock_faiss_index, mock_sentence_transformer):
    """
    Test fallback to sparse retrieval if dense retrieval fails (e.g., FAISS error).
    """
    mock_sentence_transformer.return_value = mock_sentence_transformer
    mock_faiss.read_index.return_value = mock_faiss_index
    mock_bm25_okapi.return_value = mock_bm25_model
    mock_ttl_cache.return_value = mock_cache

    # Simulate FAISS search raising an exception
    mock_faiss_index.search.side_effect = Exception("FAISS search error")

    retriever = HybridRetriever(
        dense_model_name="test-model",
        bm25_tokenizer=lambda x: x.split(),
        faiss_index_path="test-index.faiss",
        cache_ttl=3600
    )

    query = mock_queries[0]
    k = 2
    results = retriever.retrieve(query, mock_documents, k=k)

    # Assertions: Dense search was attempted and failed, BM25 was called.
    mock_faiss_index.search.assert_called_once()
    mock_bm25_model.get_top_n.assert_called_once()

    # Only BM25 results should be present, ordered by BM25 score
    assert len(results) == k
    assert results[0]["document"] == mock_documents[0] # Doc 0 (BM25 score 0.8)
    assert results[1]["document"] == mock_documents[3] # Doc 3 (BM25 score 0.5)
    assert results[0]["score"] == 0.8 * retriever.sparse_weight # Only sparse weight applied
    assert results[1]["score"] == 0.5 * retriever.sparse_weight

@patch('src.K.hybrid_retriever.hybrid_retriever.SentenceTransformer')
@patch('src.K.hybrid_retriever.hybrid_retriever.faiss')
@patch('src.K.hybrid_retriever.hybrid_retriever.BM25Okapi')
@patch('src.K.hybrid_retriever.hybrid_retriever.TTLCache')
def test_retrieve_with_cache_hit(mock_ttl_cache, mock_bm25_okapi, mock_faiss, mock_sentence_transformer,
                                 mock_documents, mock_queries, mock_bm25_model, mock_faiss_index, mock_sentence_transformer):
    """
    Test that query embedding is retrieved from cache if available.
    """
    mock_sentence_transformer.return_value = mock_sentence_transformer
    mock_faiss.read_index.return_value = mock_faiss_index
    mock_bm25_okapi.return_value = mock_bm25_model
    mock_ttl_cache.return_value = mock_cache

    # Simulate cache hit for the query embedding
    query_embedding_from_cache = np.array([0.9, 0.1, 0.1])
    mock_cache.__contains__.return_value = True
    mock_cache.__getitem__.return_value = query_embedding_from_cache

    retriever = HybridRetriever(
        dense_model_name="test-model",
        bm25_tokenizer=lambda x: x.split(),
        faiss_index_path="test-index.faiss",
        cache_ttl=3600
    )

    query = mock_queries[0]
    k = 1
    results = retriever.retrieve(query, mock_documents, k=k)

    # Assertions: SentenceTransformer.encode should NOT be called for the query
    mock_sentence_transformer.encode.assert_not_called()
    mock_cache.__contains__.assert_called_once_with(query)
    mock_cache.__getitem__.assert_called_once_with(query)
    mock_cache.__setitem__.assert_not_called() # Should not set if it was a hit

    # Other calls should still happen
    mock_faiss_index.search.assert_called_once_with(np.expand_dims(query_embedding_from_cache, axis=0), k)
    mock_bm25_model.get_top_n.assert_called_once()
    assert len(results) == k

@patch('src.K.hybrid_retriever.hybrid_retriever.SentenceTransformer')
@patch('src.K.hybrid_retriever.hybrid_retriever.faiss')
@patch('src.K.hybrid_retriever.hybrid_retriever.BM25Okapi')
@patch('src.K.hybrid_retriever.hybrid_retriever.TTLCache')
def test_retrieve_empty_documents(mock_ttl_cache, mock_bm25_okapi, mock_faiss, mock_sentence_transformer,
                                  mock_queries, mock_bm25_model, mock_faiss_index, mock_sentence_transformer):
    """
    Test retrieval with an empty list of documents.
    """
    mock_sentence_transformer.return_value = mock_sentence_transformer
    mock_faiss.read_index.return_value = mock_faiss_index
    mock_bm25_okapi.return_value = mock_bm25_model
    mock_ttl_cache.return_value = mock_cache

    retriever = HybridRetriever(
        dense_model_name="test-model",
        bm25_tokenizer=lambda x: x.split(),
        faiss_index_path="test-index.faiss",
        cache_ttl=3600
    )

    query = mock_queries[0]
    k = 1
    results = retriever.retrieve(query, [], k=k) # Empty documents list

    assert results == []
    # BM25 should still be initialized, but get_top_n might not be called or return empty
    mock_bm25_model.get_top_n.assert_called_once_with(query, [], k)
    # Dense search should not be called if there are no documents to search against
    mock_faiss_index.search.assert_not_called()

@patch('src.K.hybrid_retriever.hybrid_retriever.SentenceTransformer')
@patch('src.K.hybrid_retriever.hybrid_retriever.faiss')
@patch('src.K.hybrid_retriever.hybrid_retriever.BM25Okapi')
@patch('src.K.hybrid_retriever.hybrid_retriever.TTLCache')
def test_retrieve_empty_query(mock_ttl_cache, mock_bm25_okapi, mock_faiss, mock_sentence_transformer,
                              mock_documents, mock_bm25_model, mock_faiss_index, mock_sentence_transformer):
    """
    Test retrieval with an empty query string.
    """
    mock_sentence_transformer.return_value = mock_sentence_transformer
    mock_faiss.read_index.return_value = mock_faiss_index
    mock_bm25_okapi.return_value = mock_bm25_model
    mock_ttl_cache.return_value = mock_cache

    retriever = HybridRetriever(
        dense_model_name="test-model",
        bm25_tokenizer=lambda x: x.split(),
        faiss_index_path="test-index.faiss",
        cache_ttl=3600
    )

    query = ""
    k = 1
    results = retriever.retrieve(query, mock_documents, k=k)

    assert results == []
    mock_sentence_transformer.encode.assert_not_called() # No query to encode
    mock_faiss_index.search.assert_not_called() # No dense search
    mock_bm25_model.get_top_n.assert_not_called() # No sparse search

# Add more tests as needed:
# - Test different k values.
# - Test edge cases for score combination (e.g., one component returns no results).
# - Test BM25 tokenizer integration (if it's more complex than lambda x: x.split()).
# - Test error handling for model loading or index loading.