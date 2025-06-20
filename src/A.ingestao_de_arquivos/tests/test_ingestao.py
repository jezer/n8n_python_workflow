import os
import tempfile
import shutil
import pytest
from unittest import mock
from pathlib import Path

from .ingestao import IngestaoDeArquivos

@pytest.fixture
def temp_dir_with_files():
    temp_dir = tempfile.mkdtemp()
    files = {
        "test.txt": "Texto simples para teste.",
        "test.md": "# Markdown\nConteúdo de teste.",
        "test.json": '{"chave": "valor"}',
    }
    for fname, content in files.items():
        with open(os.path.join(temp_dir, fname), "w", encoding="utf-8") as f:
            f.write(content)
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def ingestao_instance(tmp_path):
    return IngestaoDeArquivos(output_path=str(tmp_path), log_level=20)

def test_process_file_txt(ingestao_instance, temp_dir_with_files):
    file_path = os.path.join(temp_dir_with_files, "test.txt")
    result = ingestao_instance.process_file(file_path)
    assert result is not None
    assert result["nome_arquivo"] == "test.txt"
    assert "conteudo" in result
    assert "metadados" in result
    assert result["metadados"]["formato"] == "txt"

def test_process_file_md(ingestao_instance, temp_dir_with_files):
    file_path = os.path.join(temp_dir_with_files, "test.md")
    result = ingestao_instance.process_file(file_path)
    assert result is not None
    assert result["nome_arquivo"] == "test.md"
    assert "conteudo" in result
    assert result["metadados"]["formato"] == "md"

def test_process_file_json(ingestao_instance, temp_dir_with_files):
    file_path = os.path.join(temp_dir_with_files, "test.json")
    result = ingestao_instance.process_file(file_path)
    assert result is not None
    assert result["nome_arquivo"] == "test.json"
    assert "conteudo" in result
    assert result["metadados"]["formato"] == "json"

def test_process_file_inexistente(ingestao_instance):
    result = ingestao_instance.process_file("arquivo_inexistente.txt")
    assert result is None

def test_process_file_formato_nao_suportado(ingestao_instance, tmp_path):
    file_path = tmp_path / "arquivo.unsupported"
    file_path.write_text("conteudo")
    result = ingestao_instance.process_file(str(file_path))
    assert result is None

def test_process_directory_happy_path(ingestao_instance, temp_dir_with_files):
    docs = ingestao_instance.process_directory(temp_dir_with_files)
    assert isinstance(docs, list)
    assert len(docs) == 3
    nomes = [doc["nome_arquivo"] for doc in docs]
    assert "test.txt" in nomes
    assert "test.md" in nomes
    assert "test.json" in nomes

def test_process_directory_vazio(ingestao_instance, tmp_path):
    docs = ingestao_instance.process_directory(str(tmp_path))
    assert docs == []

def test_process_file_mock_ocr_llm(ingestao_instance, temp_dir_with_files):
    file_path = os.path.join(temp_dir_with_files, "test.txt")
    mock_ocr = mock.Mock(return_value="Texto OCR simulado")
    mock_llm = mock.Mock(side_effect=lambda x: x + "\nLLM OK")
    result = ingestao_instance.process_file(file_path, ocr_func=mock_ocr, llm_func=mock_llm)
    assert "LLM OK" in result["conteudo"]

def test_process_file_arquivo_vazio(ingestao_instance, tmp_path):
    file_path = tmp_path / "vazio.txt"
    file_path.write_text("")
    result = ingestao_instance.process_file(str(file_path))
    assert result is not None
    assert result["conteudo"] == ""

def test_process_directory_min_size(ingestao_instance, temp_dir_with_files):
    # Todos arquivos têm menos de 100 bytes
    docs = ingestao_instance.process_directory(temp_dir_with_files, min_size=100)
    assert docs == []

def test_process_file_save_markdown(ingestao_instance, temp_dir_with_files, tmp_path):
    file_path = os.path.join(temp_dir_with_files, "test.txt")
    ingestao_instance.output_path = tmp_path
    result = ingestao_instance.process_file(file_path, save_markdown=True)
    output_file = tmp_path / "test.md"
    assert output_file.exists()

def test_process_file_encoding_latin1(ingestao_instance, tmp_path):
    file_path = tmp_path / "latin1.txt"
    with open(file_path, "w", encoding="latin1") as f:
        f.write("çãõáéíóú")
    result = ingestao_instance.process_file(str(file_path))
    assert result is not None
    assert "ç" in result["conteudo"]

def test_process_file_exception_handling(ingestao_instance, tmp_path):
    # Simula erro de leitura
    file_path = tmp_path / "erro.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("erro")
    with mock.patch("builtins.open", side_effect=Exception("Erro simulado")):
        result = ingestao_instance.process_file(str(file_path))
        assert result is None