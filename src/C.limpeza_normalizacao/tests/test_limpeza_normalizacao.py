import pytest
import logging
from C.limpeza_normalizacao.limpeza_normalizacao import LimpezaNormalizacao

class MockClassificador:
    def __init__(self, lixo=False, raise_exc=False):
        self.lixo = lixo
        self.raise_exc = raise_exc
    def predict(self, texto):
        if self.raise_exc:
            raise Exception("Erro simulado no classificador")
        return self.lixo

@pytest.fixture
def logger():
    return logging.getLogger("pytest_limpeza")

@pytest.mark.parametrize("entrada,esperado", [
    # Happy path: texto limpo, com cabeçalho/rodapé
    (
        [{"conteudo": "Página 1\nConteúdo válido.\nCopyright 2024"}],
        ["Conteúdo válido."]
    ),
    # Edge: só cabeçalho/rodapé
    (
        [{"conteudo": "Página 1\nCopyright 2024"}],
        []
    ),
    # Edge: texto muito curto
    (
        [{"conteudo": "abc"}],
        []
    ),
    # Edge: só caracteres gráficos
    (
        [{"conteudo": "■■■"}],
        []
    ),
    # Edge: só símbolos
    (
        [{"conteudo": "!!!!!!!!!"}],
        []
    ),
    # Edge: URL curta
    (
        [{"conteudo": "https://site.com"}],
        []
    ),
    # Edge: dicionário sem chave "conteudo"
    (
        [{}],
        []
    ),
    # Happy path: texto com encoding estranho
    (
        [{"conteudo": "Café com açúcar"}],
        ["Café com açúcar"]
    ),
    # Happy path: texto limpo, sem cabeçalho/rodapé
    (
        [{"conteudo": "Texto limpo e válido."}],
        ["Texto limpo e válido."]
    ),
])
def test_run_heuristica(entrada, esperado, logger):
    limpeza = LimpezaNormalizacao(logger=logger)
    docs = limpeza.run(entrada)
    assert [d["conteudo"] for d in docs] == esperado
# ...existing code...

def test_run_classificador_binario_lixo(logger):
    limpeza = LimpezaNormalizacao(classificador_binario=MockClassificador(lixo=True), logger=logger)
    entrada = [{"conteudo": "Conteúdo válido, mas classificador diz que é lixo."}]
    docs = limpeza.run(entrada)
    assert docs == []

def test_run_classificador_binario_valido(logger):
    limpeza = LimpezaNormalizacao(classificador_binario=MockClassificador(lixo=False), logger=logger)
    entrada = [{"conteudo": "Conteúdo válido, classificador aprova."}]
    docs = limpeza.run(entrada)
    assert [d["conteudo"] for d in docs] == ["Conteúdo válido, classificador aprova."]

def test_run_classificador_binario_exception(logger):
    limpeza = LimpezaNormalizacao(classificador_binario=MockClassificador(raise_exc=True), logger=logger)
    entrada = [{"conteudo": "Texto que gera exceção no classificador."}]
    docs = limpeza.run(entrada)
    # Deve cair no fallback heurístico, que remove textos curtos
    assert docs == []

def test_run_lista_vazia(logger):
    limpeza = LimpezaNormalizacao(logger=logger)
    docs = limpeza.run([])
    assert docs == []

def test_run_none(logger):
    limpeza = LimpezaNormalizacao(logger=logger)
    docs = limpeza.run(None)
    assert docs == []

def test_run_nao_lista(logger):
    limpeza = LimpezaNormalizacao(logger=logger)
    docs = limpeza.run("string não é lista")
    assert docs == []

def test_run_documento_sem_conteudo(logger):
    limpeza = LimpezaNormalizacao(logger=logger)
    entrada = [{"outro_campo": "valor"}]
    docs = limpeza.run(entrada)
    assert docs == []

def test_run_documento_multiplos_campos(logger):
    limpeza = LimpezaNormalizacao(logger=logger)
    entrada = [{"conteudo": "Texto válido.", "extra": 123}]
    docs = limpeza.run(entrada)
    assert [d["conteudo"] for d in docs] == ["Texto válido."]


# ...existing code...

def test_run_documento_unicode(logger):
    limpeza = LimpezaNormalizacao(logger=logger)
    entrada = [{"conteudo": "áéíóú çãõ"}]
    docs = limpeza.run(entrada)
    assert [d["conteudo"] for d in docs] == ["áéíóú çãõ"]