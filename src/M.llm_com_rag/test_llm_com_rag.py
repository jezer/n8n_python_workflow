import pytest
from unittest.mock import MagicMock, patch, call
import numpy as np

# Assume a classe está em src.M.llm_com_rag.llm_com_rag
from src.M.llm_com_rag.llm_com_rag import LLMcomRAG

# --- Fixtures para Dados e Dependências Simuladas ---

@pytest.fixture
def mock_reranker_results():
    """Simula a entrada da etapa de Reranker."""
    return [
        {
            "query": "O que é IA?",
            "resultados": [
                {"document": "Documento sobre IA.", "score": 0.95},
                {"document": "Outro documento.", "score": 0.80},
            ]
        },
        {
            "query": "O que são redes neurais?",
            "resultados": [
                {"document": "Documento sobre redes neurais.", "score": 0.98},
            ]
        }
    ]

@pytest.fixture
def mock_few_shot_examples():
    """Fornece um conjunto consistente de exemplos few-shot para os testes."""
    return [
        {"query": "O que é inteligência artificial?", "answer": "É um campo da ciência da computação."},
        {"query": "O que é um transformer?", "answer": "É uma arquitetura de rede neural."},
        {"query": "Qual a capital da França?", "answer": "Paris."},
    ]

@pytest.fixture
def mock_embedder_model(mock_few_shot_examples):
    """Simula o modelo SentenceTransformer usado para a seleção few-shot."""
    mock_embedder = MagicMock()
    
    example_queries = [ex['query'] for ex in mock_few_shot_examples]
    mock_few_shot_embeddings = np.array([
        [1.0, 0.0, 0.0], # IA
        [0.0, 1.0, 0.0], # Transformer
        [0.0, 0.0, 1.0], # França
    ])

    def encode_side_effect(texts, convert_to_tensor=False):
        if isinstance(texts, str): # Consulta única
            if "IA" in texts or "inteligência artificial" in texts:
                return np.array([0.9, 0.1, 0.1])
            if "redes neurais" in texts:
                return np.array([0.1, 0.8, 0.1]) # Similar a transformer
            return np.array([0.5, 0.5, 0.5])
        if texts == example_queries: # Codificação inicial dos exemplos
            return mock_few_shot_embeddings
        return np.array([[0.5, 0.5, 0.5]] * len(texts))

    mock_embedder.encode.side_effect = encode_side_effect
    return mock_embedder, mock_few_shot_embeddings

# --- Testes para LLMcomRAG ---

@patch('src.M.llm_com_rag.llm_com_rag.SentenceTransformer')
def test_llm_rag_init(mock_sentence_transformer_class, mock_embedder_model, mock_few_shot_examples):
    """Testa a inicialização bem-sucedida da classe LLMcomRAG."""
    mock_embedder, mock_embeddings = mock_embedder_model
    mock_sentence_transformer_class.return_value = mock_embedder

    llm_rag = LLMcomRAG(few_shot_examples=mock_few_shot_examples)

    mock_sentence_transformer_class.assert_called_once()
    assert llm_rag.embedder is not None
    assert llm_rag.few_shot_examples == mock_few_shot_examples
    assert llm_rag.few_shot_embeddings is not None
    llm_rag.embedder.encode.assert_called_once_with(
        [ex['query'] for ex in mock_few_shot_examples], convert_to_tensor=True
    )

@patch('src.M.llm_com_rag.llm_com_rag.SentenceTransformer')
def test_selecionar_exemplos_few_shot_happy_path(mock_sentence_transformer_class, mock_embedder_model, mock_few_shot_examples):
    """Testa se a seleção dinâmica few-shot encontra os exemplos mais similares."""
    mock_embedder, _ = mock_embedder_model
    mock_sentence_transformer_class.return_value = mock_embedder

    llm_rag = LLMcomRAG(few_shot_examples=mock_few_shot_examples, similarity_threshold=0.6)
    
    query = "O que é IA?"
    selected = llm_rag._selecionar_exemplos_few_shot(query, k=1)
    
    assert len(selected) == 1
    assert selected[0]['query'] == "O que é inteligência artificial?"

@patch('src.M.llm_com_rag.llm_com_rag.SentenceTransformer')
def test_selecionar_exemplos_fallback(mock_sentence_transformer_class, mock_embedder_model, mock_few_shot_examples):
    """Testa o fallback para exemplos genéricos quando a similaridade é baixa."""
    mock_embedder, _ = mock_embedder_model
    mock_sentence_transformer_class.return_value = mock_embedder

    llm_rag = LLMcomRAG(few_shot_examples=mock_few_shot_examples, similarity_threshold=0.95)
    
    query = "O que é IA?"
    selected = llm_rag._selecionar_exemplos_few_shot(query, k=2)
    
    assert len(selected) == 2
    assert selected[0] == mock_few_shot_examples[0]
    assert selected[1] == mock_few_shot_examples[1]

def test_construir_prompt():
    """Testa a lógica de construção do prompt."""
    llm_rag = LLMcomRAG(few_shot_examples=[])
    llm_rag.embedder = None

    query = "Minha Pergunta"
    context = ["Contexto 1.", "Contexto 2."]
    examples = [{"query": "Ex Q", "answer": "Ex A"}]
    
    prompt = llm_rag._construir_prompt(query, context, examples)
    
    assert "--- Exemplos ---" in prompt
    assert "Pergunta: Ex Q" in prompt
    assert "Resposta: Ex A" in prompt
    assert "--- Contexto ---" in prompt
    assert "Documento [1]: Contexto 1." in prompt
    assert "Documento [2]: Contexto 2." in prompt
    assert "--- Pergunta do Usuário ---" in prompt
    assert "Pergunta: Minha Pergunta" in prompt

@patch('src.M.llm_com_rag.llm_com_rag.LLMcomRAG._chamar_llm')
@patch('src.M.llm_com_rag.llm_com_rag.SentenceTransformer')
def test_run_happy_path(mock_sentence_transformer_class, mock_chamar_llm, mock_embedder_model, mock_reranker_results, mock_few_shot_examples):
    """Testa o método principal `run` orquestrando o processo RAG."""
    mock_embedder, _ = mock_embedder_model
    mock_sentence_transformer_class.return_value = mock_embedder
    
    mock_chamar_llm.return_value = "Resposta gerada pelo LLM."

    llm_rag = LLMcomRAG(few_shot_examples=mock_few_shot_examples)
    
    results = llm_rag.run(mock_reranker_results)

    assert len(results) == len(mock_reranker_results)
    assert mock_chamar_llm.call_count == len(mock_reranker_results)
    
    assert results[0]["query"] == "O que é IA?"
    assert results[0]["answer"] == "Resposta gerada pelo LLM."
    assert len(results[0]["context_documents"]) == 2
    assert "Documento sobre IA." in results[0]["prompt_used"]

@patch('src.M.llm_com_rag.llm_com_rag.LLMcomRAG._chamar_llm')
@patch('src.M.llm_com_rag.llm_com_rag.SentenceTransformer')
def test_run_llm_call_failure(mock_sentence_transformer_class, mock_chamar_llm, mock_embedder_model, mock_reranker_results, mock_few_shot_examples):
    """Testa se o método run lida com exceções da chamada ao LLM."""
    mock_embedder, _ = mock_embedder_model
    mock_sentence_transformer_class.return_value = mock_embedder
    
    error_message = "API indisponível"
    mock_chamar_llm.side_effect = Exception(error_message)

    llm_rag = LLMcomRAG(few_shot_examples=mock_few_shot_examples)
    
    results = llm_rag.run(mock_reranker_results)

    assert len(results) == len(mock_reranker_results)
    assert "Erro ao gerar resposta" in results[0]["answer"]
    assert error_message in results[0]["answer"]

# Adicionar mais casos de teste conforme necessário:
# - Testar com resultados vazios do reranker.
# - Testar com resultados do reranker que não têm documentos.
# - Testar falha na inicialização do modelo embedder.