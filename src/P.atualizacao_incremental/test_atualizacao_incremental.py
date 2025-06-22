import pytest
from unittest.mock import MagicMock, patch, call
import numpy as np
import os

# Assume the class is in src.P.atualizacao_incremental.atualizacao_incremental
# Adjust the import path if the file/class name is different.
from src.P.atualizacao_incremental.atualizacao_incremental import AtualizacaoIncremental

MOCK_INDEX_BASE_PATH = "./test_indices_incremental"
MOCK_EMBEDDING_DIM = 10

@pytest.fixture
def mock_old_embeddings():
    """Embeddings antigos simulados."""
    return np.random.rand(10, MOCK_EMBEDDING_DIM).astype(np.float32)

@pytest.fixture
def mock_new_data_embeddings():
    """Novos dados de embeddings simulados (vindos da etapa H)."""
    return [
        {"embedding": np.random.rand(MOCK_EMBEDDING_DIM).astype(np.float32), "referencia": "nova_ref_1"},
        {"embedding": np.random.rand(MOCK_EMBEDDING_DIM).astype(np.float32), "referencia": "nova_ref_2"},
    ]

@pytest.fixture
def mock_queries():
    """Consultas simuladas para cálculo de recall."""
    return np.random.rand(3, MOCK_EMBEDDING_DIM).astype(np.float32)

@pytest.fixture
def mock_ground_truth():
    """Ground truth simulado (índices dos documentos relevantes para cada consulta)."""
    return [[0], [1], [2]] # Exemplo: query 0 -> doc 0, query 1 -> doc 1, etc.

@pytest.fixture(autouse=True)
def cleanup_test_artifacts():
    """Garante que o diretório de teste esteja limpo antes e depois dos testes."""
    import shutil
    if os.path.exists(MOCK_INDEX_BASE_PATH):
        shutil.rmtree(MOCK_INDEX_BASE_PATH)
    os.makedirs(MOCK_INDEX_BASE_PATH, exist_ok=True)
    yield
    if os.path.exists(MOCK_INDEX_BASE_PATH):
        shutil.rmtree(MOCK_INDEX_BASE_PATH)

# --- Tests for AtualizacaoIncremental ---

def test_atualizacao_incremental_init():
    """Testa a inicialização bem-sucedida."""
    atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH, recall_threshold_drop=0.05)
    assert atualizador.index_base_path == MOCK_INDEX_BASE_PATH
    assert atualizador.recall_threshold_drop == 0.05
    assert os.path.exists(MOCK_INDEX_BASE_PATH) # Should create the directory

@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.load')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.os.path.exists', return_value=True)
def test_carregar_embeddings_success(mock_os_exists, mock_np_load, mock_old_embeddings):
    """Testa o carregamento bem-sucedido de embeddings antigos."""
    mock_np_load.return_value = mock_old_embeddings
    atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH)
    
    embeddings = atualizador.carregar_embeddings("v001")
    
    expected_path = os.path.join(MOCK_INDEX_BASE_PATH, "embeddings_v001.npy")
    mock_os_exists.assert_called_once_with(expected_path)
    mock_np_load.assert_called_once_with(expected_path)
    np.testing.assert_array_equal(embeddings, mock_old_embeddings)

@patch('src.P.atualizacao_incremental.atualizacao_incremental.os.path.exists', return_value=False)
def test_carregar_embeddings_not_found(mock_os_exists):
    """Testa o carregamento quando o arquivo de embeddings não é encontrado."""
    atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH)
    
    embeddings = atualizador.carregar_embeddings("non_existent_v")
    
    assert embeddings is None
    mock_os_exists.assert_called_once()

@patch('src.P.atualizacao_incremental.atualizacao_incremental.faiss')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.save')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.load')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.os.path.exists', side_effect=[True, False, False]) # old_emb exists, new index/meta don't
def test_run_happy_path(mock_os_exists, mock_np_load, mock_np_save, mock_faiss,
                         mock_old_embeddings, mock_new_data_embeddings, mock_queries, mock_ground_truth):
    """
    Testa o fluxo completo de atualização incremental com sucesso.
    Simula recall melhorando ou mantendo-se estável.
    """
    mock_np_load.return_value = mock_old_embeddings
    
    # Mock do IndexacaoVetorial para _calcular_recall
    mock_indexer_instance = MagicMock()
    mock_faiss.IndexFlatL2.return_value = mock_indexer_instance
    mock_indexer_instance.search.return_value = (np.array([[0.1, 0.2]]), np.array([[0, 1]])) # Simula resultados de busca

    # Simula recall: old_recall = 0.7, new_recall = 0.8 (melhora)
    with patch('src.P.atualizacao_incremental.atualizacao_incremental.AtualizacaoIncremental._calcular_recall', side_effect=[0.7, 0.8]) as mock_calcular_recall:
        atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH, recall_threshold_drop=0.05)
        
        result = atualizador.run(
            mock_old_embeddings,
            mock_new_data_embeddings,
            mock_queries,
            mock_ground_truth,
            versao_atual="v001",
            versao_nova="v002"
        )

        assert result["status"] == "success"
        assert result["old_recall"] == 0.7
        assert result["new_recall"] == 0.8
        assert result["rollback_triggered"] is False

        # Verifica se os novos embeddings e metadados foram salvos
        expected_combined_embeddings = np.vstack([mock_old_embeddings, np.array([d["embedding"] for d in mock_new_data_embeddings])])
        mock_np_save.assert_called_once_with(os.path.join(MOCK_INDEX_BASE_PATH, "embeddings_v002.npy"), expected_combined_embeddings)
        
        # Verifica se o novo índice FAISS foi construído e salvo
        mock_faiss.IndexFlatL2.assert_called_once_with(MOCK_EMBEDDING_DIM)
        mock_indexer_instance.add.assert_called_once_with(expected_combined_embeddings)
        mock_faiss.write_index.assert_called_once_with(mock_indexer_instance, os.path.join(MOCK_INDEX_BASE_PATH, "index_v002.faiss"))
        
        # Verifica chamadas de recall
        mock_calcular_recall.assert_has_calls([
            call(mock_old_embeddings, mock_queries, mock_ground_truth), # Old recall
            call(expected_combined_embeddings, mock_queries, mock_ground_truth) # New recall
        ])

@patch('src.P.atualizacao_incremental.atualizacao_incremental.faiss')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.save')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.load')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.os.path.exists', side_effect=[True, False, False])
def test_run_recall_drop_triggers_rollback(mock_os_exists, mock_np_load, mock_np_save, mock_faiss,
                                            mock_old_embeddings, mock_new_data_embeddings, mock_queries, mock_ground_truth):
    """
    Testa se uma queda significativa no recall dispara o rollback.
    """
    mock_np_load.return_value = mock_old_embeddings
    
    # Simula recall: old_recall = 0.8, new_recall = 0.7 (queda de 0.1, > threshold de 0.05)
    with patch('src.P.atualizacao_incremental.atualizacao_incremental.AtualizacaoIncremental._calcular_recall', side_effect=[0.8, 0.7]) as mock_calcular_recall:
        atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH, recall_threshold_drop=0.05)
        
        result = atualizador.run(
            mock_old_embeddings,
            mock_new_data_embeddings,
            mock_queries,
            mock_ground_truth,
            versao_atual="v001",
            versao_nova="v002"
        )

        assert result["status"] == "rollback_triggered"
        assert result["old_recall"] == 0.8
        assert result["new_recall"] == 0.7
        assert result["rollback_triggered"] is True

        # Verifica se os novos embeddings/índice NÃO foram salvos (rollback)
        mock_np_save.assert_not_called()
        mock_faiss.write_index.assert_not_called()

@patch('src.P.atualizacao_incremental.atualizacao_incremental.faiss')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.save')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.load')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.os.path.exists', side_effect=[True, False, False])
def test_run_no_new_data(mock_os_exists, mock_np_load, mock_np_save, mock_faiss,
                         mock_old_embeddings, mock_queries, mock_ground_truth):
    """Testa o método run quando não há novos dados de embeddings."""
    mock_np_load.return_value = mock_old_embeddings
    
    with patch('src.P.atualizacao_incremental.atualizacao_incremental.AtualizacaoIncremental._calcular_recall', return_value=0.7) as mock_calcular_recall:
        atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH, recall_threshold_drop=0.05)
        
        result = atualizador.run(
            mock_old_embeddings,
            [], # Sem novos dados
            mock_queries,
            mock_ground_truth,
            versao_atual="v001",
            versao_nova="v002"
        )

        assert result["status"] == "no_new_data"
        assert result["old_recall"] == 0.7
        assert result["new_recall"] == 0.7 # Recall deve ser o mesmo
        assert result["rollback_triggered"] is False

        mock_np_save.assert_not_called() # Não deve salvar novos embeddings
        mock_faiss.write_index.assert_not_called() # Não deve salvar novo índice
        mock_calcular_recall.assert_called_once() # Apenas o recall antigo é calculado

@patch('src.P.atualizacao_incremental.atualizacao_incremental.faiss')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.save')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.np.load')
@patch('src.P.atualizacao_incremental.atualizacao_incremental.os.path.exists', side_effect=[True, False, False])
def test_run_no_ground_truth_skips_recall_check(mock_os_exists, mock_np_load, mock_np_save, mock_faiss,
                                                 mock_old_embeddings, mock_new_data_embeddings, mock_queries):
    """
    Testa que o cálculo de recall é ignorado se ground_truth não for fornecido.
    """
    mock_np_load.return_value = mock_old_embeddings
    
    with patch('src.P.atualizacao_incremental.atualizacao_incremental.AtualizacaoContinua') as MockAvaliacaoContinua:
        atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH, recall_threshold_drop=0.05)
        
        result = atualizador.run(
            mock_old_embeddings,
            mock_new_data_embeddings,
            mock_queries,
            None, # Sem ground_truth
            versao_atual="v001",
            versao_nova="v002"
        )

        assert result["status"] == "success_no_recall_check"
        assert result["old_recall"] is None
        assert result["new_recall"] is None
        assert result["rollback_triggered"] is False

        # Verifica que o AvaliacaoContinua não foi instanciado para calcular recall
        MockAvaliacaoContinua.assert_not_called()
        
        # Verifica que os novos embeddings e índice foram salvos (sem rollback)
        mock_np_save.assert_called_once()
        mock_faiss.write_index.assert_called_once()

@patch('src.P.atualizacao_incremental.atualizacao_incremental.faiss')
def test_calcular_recall(mock_faiss):
    """Testa a função auxiliar _calcular_recall."""
    mock_embeddings = np.random.rand(10, MOCK_EMBEDDING_DIM).astype(np.float32)
    mock_queries = np.random.rand(3, MOCK_EMBEDDING_DIM).astype(np.float32)
    mock_ground_truth = [[0], [1], [2]] # Query 0 expects doc 0, etc.

    mock_index = MagicMock()
    mock_faiss.IndexFlatL2.return_value = mock_index
    
    # Simula que a busca retorna o documento correto para cada query
    mock_index.search.side_effect = [
        (np.array([[0.1, 0.2]]), np.array([[0, 5]])), # Query 0, finds doc 0
        (np.array([[0.05, 0.3]]), np.array([[1, 6]])), # Query 1, finds doc 1
        (np.array([[0.1, 0.4]]), np.array([[2, 7]])), # Query 2, finds doc 2
    ]

    atualizador = AtualizacaoIncremental(index_base_path=MOCK_INDEX_BASE_PATH)
    recall = atualizador._calcular_recall(mock_embeddings, mock_queries, mock_ground_truth, k=5)

    assert recall == 1.0 # 3 de 3 queries tiveram o doc correto no top-k
    mock_faiss.IndexFlatL2.assert_called_once_with(MOCK_EMBEDDING_DIM)
    mock_index.add.assert_called_once_with(mock_embeddings)
    assert mock_index.search.call_count == len(mock_queries)

# Adicionar mais testes conforme necessário:
# - Testar com embeddings de dimensões inconsistentes (se _calcular_recall ou run não filtrarem).
# - Testar cenários de erro durante o salvamento de arquivos.
# - Testar o caso onde carregar_embeddings retorna None.