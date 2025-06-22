import pytest
from unittest.mock import MagicMock, patch

# Assume a classe está em src.Q.otimizacao_prompts.otimizacao_prompts
from src.Q.otimizacao_prompts.otimizacao_prompts import OtimizacaoPrompts

# --- Fixtures para Dados e Dependências Simuladas ---

@pytest.fixture
def mock_evaluation_results():
    """Simula a entrada da etapa de Avaliação Contínua."""
    return [
        {
            "query": "O que é IA?",
            "answer": "IA é um campo da ciência da computação.",
            "context_documents": ["Doc 1: IA é um campo..."],
            "avaliacao_llm_judge": "Boa resposta."
        },
        {
            "query": "Qual a capital da França?",
            "answer": "Paris.",
            "context_documents": ["Doc 2: A capital da França é Paris."],
            "avaliacao_llm_judge": "Correto."
        }
    ]

@pytest.fixture
def mock_referencias():
    """Simula as respostas de referência (ground truth)."""
    return [
        {"query": "O que é IA?", "answer": "Inteligência Artificial é o ramo da ciência da computação que busca criar máquinas capazes de pensar como humanos."},
        {"query": "Qual a capital da França?", "answer": "A capital da França é Paris."},
    ]

@pytest.fixture
def mock_llm_client():
    """Simula um cliente LLM que responde de forma diferente para cada prompt."""
    mock_llm = MagicMock()
    
    def generate_response(prompt: str) -> str:
        if "Prompt A" in prompt:
            if "IA" in prompt:
                return "IA é um campo da ciência da computação." # Resposta curta
            if "França" in prompt:
                return "Paris." # Resposta curta
        elif "Prompt B" in prompt:
            if "IA" in prompt:
                return "Inteligência Artificial, ou IA, é o ramo da ciência da computação que busca criar máquinas capazes de pensar como humanos." # Resposta longa
            if "França" in prompt:
                return "A capital da França, localizada na Europa, é a cidade de Paris." # Resposta longa
        return "Resposta padrão."
        
    mock_llm.generate.side_effect = generate_response
    return mock_llm

# --- Testes para OtimizacaoPrompts ---

def test_otimizacao_prompts_init(mock_llm_client):
    """Testa a inicialização bem-sucedida da classe."""
    otimizador = OtimizacaoPrompts(llm_client=mock_llm_client)
    assert otimizador.llm_client is not None

def test_run_ab_test_happy_path(mock_llm_client, mock_evaluation_results, mock_referencias):
    """
    Testa o fluxo principal do teste A/B, esperando que o Prompt B vença
    devido à lógica de avaliação simulada que favorece respostas mais longas.
    """
    otimizador = OtimizacaoPrompts(llm_client=mock_llm_client)
    
    # Prompts padrão da classe
    prompt_a = "Contexto:\n{context}\n\nPergunta: {query}\nPrompt A: Resposta concisa:"
    prompt_b = "Contexto fornecido:\n{context}\n\nSua tarefa é responder à seguinte pergunta do usuário com base estritamente nas informações do contexto.\nPergunta do usuário: {query}\nPrompt B: Resposta detalhada:"

    resultado = otimizador.run(
        mock_evaluation_results, 
        metodo="ab_test", 
        prompt_a=prompt_a, 
        prompt_b=prompt_b, 
        referencias=mock_referencias
    )

    assert resultado["method"] == "a/b_test"
    assert resultado["num_samples_tested"] == 2
    assert "prompt_a_avg_score" in resultado
    assert "prompt_b_avg_score" in resultado
    assert resultado["prompt_b_avg_score"] > resultado["prompt_a_avg_score"]
    assert resultado["winner"] == "Prompt B"
    
    # Verifica se o LLM foi chamado para cada prompt e cada query
    assert mock_llm_client.generate.call_count == 4 # 2 queries * 2 prompts

def test_run_ab_test_sem_referencias(mock_llm_client, mock_evaluation_results):
    """
    Testa se o teste A/B retorna um erro quando as referências não são fornecidas.
    """
    otimizador = OtimizacaoPrompts(llm_client=mock_llm_client)
    resultado = otimizador.run(mock_evaluation_results, metodo="ab_test", referencias=[])

    assert resultado["status"] == "error"
    assert "Referências não fornecidas" in resultado["message"]
    mock_llm_client.generate.assert_not_called()

def test_run_metodo_nao_implementado(mock_llm_client, mock_evaluation_results):
    """
    Testa o comportamento quando um método de otimização desconhecido é solicitado.
    """
    otimizador = OtimizacaoPrompts(llm_client=mock_llm_client)
    resultado = otimizador.run(mock_evaluation_results, metodo="star")

    assert resultado["status"] == "unimplemented_method"
    assert resultado["method"] == "star"

def test_run_ab_test_input_vazio(mock_llm_client, mock_referencias):
    """
    Testa o teste A/B com uma lista de avaliação vazia.
    """
    otimizador = OtimizacaoPrompts(llm_client=mock_llm_client)
    resultado = otimizador.run([], metodo="ab_test", referencias=mock_referencias)

    assert resultado["num_samples_tested"] == 0
    assert resultado["prompt_a_avg_score"] == 0
    assert resultado["prompt_b_avg_score"] == 0
    # O vencedor pode ser A ou B, dependendo da implementação de desempate (>=)
    assert resultado["winner"] in ["Prompt A", "Prompt B"]
    mock_llm_client.generate.assert_not_called()

def test_run_ab_test_llm_failure(mock_evaluation_results, mock_referencias):
    """
    Testa o tratamento de erro se a chamada ao LLM falhar.
    """
    mock_llm_failing = MagicMock()
    mock_llm_failing.generate.side_effect = Exception("API Error")
    
    otimizador = OtimizacaoPrompts(llm_client=mock_llm_failing)
    
    # A exceção deve ser capturada pela camada superior (main.py ou orquestrador),
    # então testamos se ela é propagada.
    with pytest.raises(Exception, match="API Error"):
        otimizador.run(mock_evaluation_results, metodo="ab_test", referencias=mock_referencias)

# Adicionar mais casos de teste conforme necessário:
# - Testar a lógica de construção do prompt com contextos complexos.
# - Testar a lógica de avaliação simulada com diferentes cenários.
# - Se o método 'star' for implementado, adicionar testes para ele.