import pytest
from unittest.mock import MagicMock, patch
import numpy as np

# Supondo que a classe está em src.J.metadados_enriquecidos.metadados_enriquecidos
# Ajuste o caminho de importação se o nome do arquivo/classe for diferente.
from src.J.metadados_enriquecidos.metadados_enriquecidos import MetadadosEnriquecidos

@pytest.fixture
def mock_resultados_indexados_validos():
    """Dados de entrada válidos simulando a saída da etapa de indexação."""
    return [
        {"id": "doc1_chunk1", "texto_chunk": "A IBM anunciou um novo processador em Nova York.", "embedding": np.array([0.1, 0.2])},
        {"id": "doc2_chunk1", "texto_chunk": "A Microsoft lançou o Windows 11.", "embedding": np.array([0.3, 0.4])},
        {"id": "doc3_chunk1", "texto_chunk": "Texto sem entidades óbvias.", "embedding": np.array([0.5, 0.6])},
    ]

@pytest.fixture
def mock_grafo_conhecimento_valido():
    """Simula um objeto de grafo de conhecimento com algumas entidades."""
    # A estrutura exata do grafo dependerá da sua implementação.
    # Para este mock, vamos assumir que podemos verificar a existência de uma entidade.
    grafo = MagicMock()
    entidades_no_grafo = {"IBM": "org_ibm_id", "Microsoft": "org_msft_id", "Nova York": "loc_nyc_id"}
    
    def get_entidade_id(nome_entidade):
        return entidades_no_grafo.get(nome_entidade)

    grafo.get_entidade_id = MagicMock(side_effect=get_entidade_id)
    return grafo

@pytest.fixture
def mock_spacy_nlp():
    """Mock para o objeto nlp do spaCy."""
    nlp = MagicMock()
    
    # Simular o processamento de texto e a extração de entidades
    def process_text(text):
        doc_mock = MagicMock()
        ents = []
        if "IBM" in text and "Nova York" in text:
            ent_ibm = MagicMock()
            ent_ibm.text = "IBM"
            ent_ibm.label_ = "ORG"
            ent_ny = MagicMock()
            ent_ny.text = "Nova York"
            ent_ny.label_ = "LOC"
            ents = [ent_ibm, ent_ny]
        elif "Microsoft" in text and "Windows 11" in text:
            ent_msft = MagicMock()
            ent_msft.text = "Microsoft"
            ent_msft.label_ = "ORG"
            ent_win = MagicMock()
            ent_win.text = "Windows 11"
            ent_win.label_ = "PRODUCT"
            ents = [ent_msft, ent_win]
        doc_mock.ents = ents
        return doc_mock

    nlp.side_effect = process_text
    return nlp

@patch('src.J.metadados_enriquecidos.metadados_enriquecidos.spacy.load') # Ajuste o caminho se spacy for importado de outra forma
def test_metadados_enriquecidos_init_success(mock_spacy_load, mock_spacy_nlp):
    """Testa a inicialização bem-sucedida e o carregamento do modelo (simulado)."""
    mock_spacy_load.return_value = mock_spacy_nlp
    
    enriquecedor = MetadadosEnriquecidos(spacy_model_name='pt_core_news_sm')
    
    mock_spacy_load.assert_called_once_with('pt_core_news_sm')
    assert enriquecedor.nlp == mock_spacy_nlp

@patch('src.J.metadados_enriquecidos.metadados_enriquecidos.spacy.load')
def test_metadados_enriquecidos_init_model_load_failure(mock_spacy_load):
    """Testa a inicialização quando o carregamento do modelo spaCy falha."""
    mock_spacy_load.side_effect = OSError("Erro ao carregar modelo")
    
    # Supondo que o construtor lida com isso definindo self.nlp como None e logando um aviso.
    # Este comportamento depende da implementação real de __init__.
    with pytest.warns(UserWarning, match="Erro ao carregar o modelo spaCy mock_fail_model: Erro ao carregar modelo"):
        enriquecedor = MetadadosEnriquecidos(spacy_model_name='mock_fail_model')
    
    assert enriquecedor.nlp is None
    mock_spacy_load.assert_called_once_with('mock_fail_model')


def test_run_happy_path_with_graph(mock_spacy_nlp, mock_resultados_indexados_validos, mock_grafo_conhecimento_valido):
    """Testa o método run com dados válidos e um grafo de conhecimento."""
    with patch('src.J.metadados_enriquecidos.metadados_enriquecidos.spacy.load', return_value=mock_spacy_nlp):
        enriquecedor = MetadadosEnriquecidos()

    resultados = enriquecedor.run(mock_resultados_indexados_validos, grafo=mock_grafo_conhecimento_valido)

    assert len(resultados) == len(mock_resultados_indexados_validos)
    
    # Documento 1: IBM e Nova York
    assert "entidades_ner" in resultados[0]
    assert len(resultados[0]["entidades_ner"]) == 2
    assert any(ent['texto'] == "IBM" and ent['label'] == "ORG" and ent.get('link_grafo') == "org_ibm_id" for ent in resultados[0]["entidades_ner"])
    assert any(ent['texto'] == "Nova York" and ent['label'] == "LOC" and ent.get('link_grafo') == "loc_nyc_id" for ent in resultados[0]["entidades_ner"])

    # Documento 2: Microsoft e Windows 11
    assert "entidades_ner" in resultados[1]
    assert len(resultados[1]["entidades_ner"]) == 2
    assert any(ent['texto'] == "Microsoft" and ent['label'] == "ORG" and ent.get('link_grafo') == "org_msft_id" for ent in resultados[1]["entidades_ner"])
    assert any(ent['texto'] == "Windows 11" and ent['label'] == "PRODUCT" and ent.get('link_grafo') is None for ent in resultados[1]["entidades_ner"]) # Windows 11 não está no mock do grafo

    # Documento 3: Sem entidades
    assert "entidades_ner" in resultados[2]
    assert len(resultados[2]["entidades_ner"]) == 0

    mock_grafo_conhecimento_valido.get_entidade_id.assert_any_call("IBM")
    mock_grafo_conhecimento_valido.get_entidade_id.assert_any_call("Nova York")
    mock_grafo_conhecimento_valido.get_entidade_id.assert_any_call("Microsoft")
    mock_grafo_conhecimento_valido.get_entidade_id.assert_any_call("Windows 11")


def test_run_sem_grafo(mock_spacy_nlp, mock_resultados_indexados_validos):
    """Testa o método run sem fornecer um grafo de conhecimento."""
    with patch('src.J.metadados_enriquecidos.metadados_enriquecidos.spacy.load', return_value=mock_spacy_nlp):
        enriquecedor = MetadadosEnriquecidos()

    resultados = enriquecedor.run(mock_resultados_indexados_validos, grafo=None)

    assert len(resultados) == len(mock_resultados_indexados_validos)
    assert "entidades_ner" in resultados[0]
    assert any(ent['texto'] == "IBM" and 'link_grafo' not in ent for ent in resultados[0]["entidades_ner"])


def test_run_input_vazio(mock_spacy_nlp):
    """Testa o método run com uma lista de entrada vazia."""
    with patch('src.J.metadados_enriquecidos.metadados_enriquecidos.spacy.load', return_value=mock_spacy_nlp):
        enriquecedor = MetadadosEnriquecidos()
    
    resultados = enriquecedor.run([], grafo=None)
    assert resultados == []
    mock_spacy_nlp.assert_not_called() # nlp não deve ser chamado se não há dados


def test_run_item_sem_texto_chunk(mock_spacy_nlp):
    """Testa o método run com um item que não possui a chave 'texto_chunk'."""
    dados_entrada = [{"id": "doc_sem_texto", "embedding": np.array([0.7,0.8])}]
    with patch('src.J.metadados_enriquecidos.metadados_enriquecidos.spacy.load', return_value=mock_spacy_nlp):
        enriquecedor = MetadadosEnriquecidos()

    resultados = enriquecedor.run(dados_entrada, grafo=None)
    assert len(resultados) == 1
    assert "entidades_ner" in resultados[0]
    assert len(resultados[0]["entidades_ner"]) == 0 # Nenhuma entidade se não há texto
    mock_spacy_nlp.assert_not_called()


def test_run_modelo_nlp_nao_carregado(mock_resultados_indexados_validos):
    """Testa o método run quando o modelo NLP (spaCy) não foi carregado."""
    # Simula falha no carregamento do modelo durante __init__
    with patch('src.J.metadados_enriquecidos.metadados_enriquecidos.spacy.load', side_effect=OSError("Falha ao carregar")):
        with pytest.warns(UserWarning): # Suprime o aviso durante a inicialização
            enriquecedor = MetadadosEnriquecidos()
    
    assert enriquecedor.nlp is None

    resultados = enriquecedor.run(mock_resultados_indexados_validos, grafo=None)
    
    # O comportamento esperado aqui é que cada item seja retornado sem 'entidades_ner'
    # ou com 'entidades_ner' vazia, e um log de aviso seja gerado.
    # A implementação atual da classe pode precisar de um try-except em torno de self.nlp(text).
    assert len(resultados) == len(mock_resultados_indexados_validos)
    for item in resultados:
        # Supondo que a classe adiciona uma lista vazia ou não adiciona a chave se o nlp falhar.
        # Isso depende da implementação exata de como o erro de nlp não carregado é tratado no run.
        assert "entidades_ner" in item
        assert item["entidades_ner"] == [] # Ou que a chave não existe, dependendo da lógica de erro.

# Adicionar mais casos de teste conforme necessário, por exemplo:
# - Testar diferentes tipos de entidades e como são tratadas.
# - Testar o comportamento quando o grafo.get_entidade_id lança uma exceção.
# - Testar textos com caracteres especiais ou em diferentes idiomas (se aplicável).