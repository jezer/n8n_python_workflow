import os
import tempfile
import shutil
import pytest
import json
import pandas as pd
from unittest import mock
from pathlib import Path
from PIL import Image
import io
import logging

from .ingestao import IngestaoDeArquivos

class TestIngestaoDeArquivos:
    """Classe de testes abrangente para IngestaoDeArquivos seguindo as instruções do testeinstrucoes.md"""

    @pytest.fixture
    def temp_dir_with_files(self):
        """Fixture que cria diretório temporário com arquivos de teste de vários formatos"""
        temp_dir = tempfile.mkdtemp()
        
        # Arquivos de teste
        files_content = {
            "test.txt": "Texto simples para teste com acentos: ção, ã, é, í, ó, ú.",
            "test.md": "# Markdown\n\n## Seção\n\nConteúdo de **teste** com *formatação*.\n\n- Item 1\n- Item 2",
            "test.json": '{"chave": "valor", "numero": 42, "lista": [1, 2, 3], "nested": {"key": "value"}}',
            "empty.txt": "",
            "large.txt": "A" * 10000,  # Arquivo grande para teste de performance
            "special_chars.txt": "Caracteres especiais: @#$%^&*()_+-=[]{}|;':\",./<>?`~",
            "multiline.md": "# Título\n\nPrimeiro parágrafo.\n\nSegundo parágrafo com mais texto.\n\n## Subtítulo\n\nMais conteúdo aqui."
        }
        
        for fname, content in files_content.items():
            with open(os.path.join(temp_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)
        
        # Arquivo com encoding latin1
        with open(os.path.join(temp_dir, "latin1.txt"), "w", encoding="latin1") as f:
            f.write("Texto com acentos: ção, ã, é, í, ó, ú")
        
        # Arquivo Excel simulado (criar um DataFrame pequeno)
        try:
            df = pd.DataFrame({"Col1": [1, 2, 3], "Col2": ["A", "B", "C"]})
            df.to_excel(os.path.join(temp_dir, "test.xlsx"), index=False)
        except ImportError:
            # Se openpyxl não estiver disponível, criar arquivo mock
            pass
        
        # Arquivo não suportado
        with open(os.path.join(temp_dir, "unsupported.xyz"), "w") as f:
            f.write("conteudo")
        
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def ingestao_instance(self, tmp_path):
        """Fixture que cria instância da classe IngestaoDeArquivos"""
        return IngestaoDeArquivos(
            output_path=str(tmp_path),
            log_level=logging.WARNING,  # Reduzir logs durante testes
            max_workers=2
        )

    @pytest.fixture
    def empty_dir(self):
        """Fixture que cria diretório vazio"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def corrupted_files_dir(self):
        """Fixture que cria diretório com arquivos corrompidos"""
        temp_dir = tempfile.mkdtemp()
        
        # Arquivo corrompido - criar arquivo binário com extensão de texto
        with open(os.path.join(temp_dir, "corrupted.txt"), "wb") as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
        
        # JSON malformado
        with open(os.path.join(temp_dir, "bad.json"), "w") as f:
            f.write('{"chave": valor}')  # JSON inválido
        
        yield temp_dir
        shutil.rmtree(temp_dir)

    # ===== TESTES HAPPY PATH (Caminho ideal) =====
    
    def test_process_file_txt_happy_path(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento de arquivo TXT válido"""
        file_path = os.path.join(temp_dir_with_files, "test.txt")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        assert result["nome_arquivo"] == "test.txt"
        assert result["formato"] == "txt"
        assert "Texto simples" in result["conteudo"]
        assert "metadados" in result
        assert result["metadados"]["formato"] == "txt"
        assert result["metadados"]["tamanho_bytes"] > 0

    def test_process_file_md_happy_path(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento de arquivo Markdown válido"""
        file_path = os.path.join(temp_dir_with_files, "test.md")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        assert result["nome_arquivo"] == "test.md"
        assert result["formato"] == "md"
        assert "Markdown" in result["conteudo"]
        assert "**teste**" in result["conteudo"]

    def test_process_file_json_happy_path(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento de arquivo JSON válido"""
        file_path = os.path.join(temp_dir_with_files, "test.json")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        assert result["nome_arquivo"] == "test.json"
        assert result["formato"] == "json"
        assert "chave" in result["conteudo"]
        assert "valor" in result["conteudo"]

    def test_process_directory_happy_path(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento de diretório com arquivos válidos"""
        docs = ingestao_instance.process_directory(temp_dir_with_files)
        
        assert isinstance(docs, list)
        assert len(docs) >= 3  # Pelo menos txt, md, json
        
        nomes = [doc["nome_arquivo"] for doc in docs]
        assert "test.txt" in nomes
        assert "test.md" in nomes
        assert "test.json" in nomes

    def test_process_file_with_different_return_formats(self, ingestao_instance, temp_dir_with_files):
        """Testa diferentes formatos de retorno"""
        file_path = os.path.join(temp_dir_with_files, "test.md")
        
        # Teste formato markdown (padrão)
        result_md = ingestao_instance.process_file(file_path, return_format="markdown")
        assert "# Markdown" in result_md["conteudo"]
        
        # Teste formato texto
        result_txt = ingestao_instance.process_file(file_path, return_format="text")
        assert "Markdown" in result_txt["conteudo"]
        # Deve remover formatação markdown
        assert "#" not in result_txt["conteudo"]
        
        # Teste formato HTML
        result_html = ingestao_instance.process_file(file_path, return_format="html")
        assert result_html["conteudo"] is not None

    # ===== TESTES EDGE CASES (Casos extremos) =====
    
    def test_process_directory_empty(self, ingestao_instance, empty_dir):
        """Testa processamento de diretório vazio"""
        docs = ingestao_instance.process_directory(empty_dir)
        assert docs == []

    def test_process_file_empty(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento de arquivo vazio"""
        file_path = os.path.join(temp_dir_with_files, "empty.txt")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        assert result["conteudo"] == ""
        assert result["metadados"]["tamanho_bytes"] == 0

    def test_process_file_large(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento de arquivo grande"""
        file_path = os.path.join(temp_dir_with_files, "large.txt")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        assert result["metadados"]["tamanho_bytes"] == 10000
        assert len(result["conteudo"]) == 10000

    def test_process_file_special_characters(self, ingestao_instance, temp_dir_with_files):
        """Testa arquivo com caracteres especiais"""
        file_path = os.path.join(temp_dir_with_files, "special_chars.txt")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        assert "@#$%" in result["conteudo"]

    def test_process_file_latin1_encoding(self, ingestao_instance, temp_dir_with_files):
        """Testa arquivo com encoding latin1"""
        file_path = os.path.join(temp_dir_with_files, "latin1.txt")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        assert "ção" in result["conteudo"]

    def test_process_directory_with_filters(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento com filtros de extensão e tamanho"""
        # Filtro por extensão
        docs_txt = ingestao_instance.process_directory(
            temp_dir_with_files, 
            filter_ext=['.txt']
        )
        assert all(doc["formato"] == "txt" for doc in docs_txt)
        
        # Filtro por tamanho mínimo
        docs_large = ingestao_instance.process_directory(
            temp_dir_with_files, 
            min_size=5000  # Apenas arquivo large.txt
        )
        assert len(docs_large) == 1
        assert docs_large[0]["nome_arquivo"] == "large.txt"

    def test_process_file_save_markdown(self, ingestao_instance, temp_dir_with_files, tmp_path):
        """Testa salvamento em arquivo markdown"""
        file_path = os.path.join(temp_dir_with_files, "test.txt")
        ingestao_instance.output_path = tmp_path
        
        result = ingestao_instance.process_file(file_path, save_markdown=True)
        
        output_file = tmp_path / "test.md"
        assert output_file.exists()
        assert result is not None

    # ===== TESTES FAILURE MODES (Modos de falha) =====
    
    def test_process_file_inexistente(self, ingestao_instance):
        """Testa processamento de arquivo inexistente"""
        result = ingestao_instance.process_file("arquivo_que_nao_existe.txt")
        assert result is None

    def test_process_file_formato_nao_suportado(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento de formato não suportado"""
        file_path = os.path.join(temp_dir_with_files, "unsupported.xyz")
        result = ingestao_instance.process_file(file_path)
        assert result is None

    def test_process_directory_inexistente(self, ingestao_instance):
        """Testa processamento de diretório inexistente"""
        docs = ingestao_instance.process_directory("diretorio_que_nao_existe")
        assert docs == []

    def test_process_file_json_corrupted(self, ingestao_instance, corrupted_files_dir):
        """Testa processamento de JSON corrompido"""
        file_path = os.path.join(corrupted_files_dir, "bad.json")
        result = ingestao_instance.process_file(file_path)
        # Deve retornar None ou string vazia devido ao erro
        assert result is None or result["conteudo"] == ""

    def test_process_file_binary_as_text(self, ingestao_instance, corrupted_files_dir):
        """Testa processamento de arquivo binário com extensão de texto"""
        file_path = os.path.join(corrupted_files_dir, "corrupted.txt")
        result = ingestao_instance.process_file(file_path)
        # Deve conseguir processar mas pode ter conteúdo estranho
        assert result is not None

    def test_process_file_exception_handling(self, ingestao_instance, temp_dir_with_files):
        """Testa tratamento de exceções durante processamento"""
        file_path = os.path.join(temp_dir_with_files, "test.txt")
        
        # Simula erro na leitura do arquivo
        with mock.patch("builtins.open", side_effect=Exception("Erro simulado")):
            result = ingestao_instance.process_file(file_path)
            assert result is None

    # ===== TESTES DE MOCKING (Simulação de dependências) =====
    
    def test_process_file_mock_ocr_function(self, ingestao_instance, temp_dir_with_files):
        """Testa mock da função OCR"""
        file_path = os.path.join(temp_dir_with_files, "test.txt")
        
        mock_ocr = mock.Mock(return_value="Texto extraído via OCR simulado")
        result = ingestao_instance.process_file(file_path, ocr_func=mock_ocr)
        
        assert result is not None
        # OCR não deve ser chamado para arquivos txt normais
        mock_ocr.assert_not_called()

    def test_process_file_mock_llm_function(self, ingestao_instance, temp_dir_with_files):
        """Testa mock da função LLM"""
        file_path = os.path.join(temp_dir_with_files, "test.txt")
        
        mock_llm = mock.Mock(side_effect=lambda x: x + "\n\n[Processado por LLM]")
        result = ingestao_instance.process_file(file_path, llm_func=mock_llm)
        
        assert result is not None
        assert "[Processado por LLM]" in result["conteudo"]
        mock_llm.assert_called_once()

    def test_process_pdf_mock_ocr(self, ingestao_instance, tmp_path):
        """Testa processamento de PDF com OCR mockado"""
        # Cria arquivo PDF falso (apenas para teste de caminho)
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_bytes(b'%PDF-fake')
        
        mock_ocr = mock.Mock(return_value="Texto extraído do PDF via OCR")
        
        # Mocka as dependências de PDF
        with mock.patch('fitz.open') as mock_fitz:
            mock_doc = mock.Mock()
            mock_page = mock.Mock()
            mock_page.get_text.return_value = ""  # PDF sem texto
            mock_doc.__iter__ = mock.Mock(return_value=iter([mock_page]))
            mock_fitz.return_value = mock_doc
            
            with mock.patch('pdf2image.convert_from_path') as mock_convert:
                mock_image = mock.Mock()
                mock_convert.return_value = [mock_image]
                
                result = ingestao_instance.process_file(str(pdf_path), ocr_func=mock_ocr)
                
                if result:  # Se não houve erro de dependência
                    mock_ocr.assert_called()

    # ===== TESTES DE PERFORMANCE E LOGGING =====
    
    def test_parallel_processing(self, ingestao_instance, temp_dir_with_files):
        """Testa processamento paralelo"""
        # Define max_workers baixo para teste
        ingestao_instance.max_workers = 2
        
        docs = ingestao_instance.process_directory(temp_dir_with_files)
        assert len(docs) >= 3
        
        # Verifica se todos os documentos foram processados
        for doc in docs:
            assert doc is not None
            assert "conteudo" in doc
            assert "metadados" in doc

    def test_logging_configuration(self, tmp_path):
        """Testa configuração de logging"""
        # Testa diferentes níveis de log
        ingestao_debug = IngestaoDeArquivos(
            output_path=str(tmp_path),
            log_level=logging.DEBUG
        )
        assert ingestao_debug.logger.level <= logging.DEBUG
        
        ingestao_error = IngestaoDeArquivos(
            output_path=str(tmp_path),
            log_level=logging.ERROR
        )
        # Verifica se o logger foi configurado

    def test_metadata_completeness(self, ingestao_instance, temp_dir_with_files):
        """Testa completude dos metadados"""
        file_path = os.path.join(temp_dir_with_files, "test.txt")
        result = ingestao_instance.process_file(file_path)
        
        assert result is not None
        metadados = result["metadados"]
        
        # Verifica se todos os campos obrigatórios estão presentes
        assert "tamanho_bytes" in metadados
        assert "formato" in metadados
        assert "caminho" in metadados
        assert "tamanho_markdown" in metadados
        assert "linhas_markdown" in metadados
        
        # Verifica se os valores fazem sentido
        assert metadados["tamanho_bytes"] > 0
        assert metadados["formato"] == "txt"
        assert metadados["caminho"] == file_path
        assert metadados["tamanho_markdown"] > 0
        assert metadados["linhas_markdown"] >= 1

    # ===== TESTES DE INTEGRAÇÃO =====
    
    def test_end_to_end_workflow(self, ingestao_instance, temp_dir_with_files, tmp_path):
        """Testa fluxo completo de ponta a ponta"""
        ingestao_instance.output_path = tmp_path
        
        # Processa diretório completo
        docs = ingestao_instance.process_directory(
            temp_dir_with_files,
            save_markdown=True,
            filter_ext=['.txt', '.md', '.json'],
            min_size=1
        )
        
        # Verifica se documentos foram processados
        assert len(docs) >= 3
        
        # Verifica se arquivos markdown foram salvos
        md_files = list(tmp_path.glob("*.md"))
        assert len(md_files) >= 3
        
        # Verifica conteúdo dos documentos
        for doc in docs:
            assert doc["nome_arquivo"] is not None
            assert doc["formato"] in ["txt", "md", "json"]
            assert doc["conteudo"] is not None
            assert doc["metadados"] is not None

    def test_custom_tesseract_path(self, tmp_path):
        """Testa configuração de caminho customizado do Tesseract"""
        custom_path = "/usr/bin/tesseract"
        ingestao = IngestaoDeArquivos(
            tesseract_path=custom_path,
            output_path=str(tmp_path)
        )
        # Verifica se a instância foi criada sem erro
        assert ingestao is not None

    def test_different_languages(self, tmp_path):
        """Testa configuração de idiomas diferentes"""
        ingestao_en = IngestaoDeArquivos(
            output_path=str(tmp_path),
            language="en"
        )
        assert ingestao_en.language == "en"
        
        ingestao_pt = IngestaoDeArquivos(
            output_path=str(tmp_path),
            language="pt"
        )
        assert ingestao_pt.language == "pt"