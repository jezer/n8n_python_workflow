import os
from pathlib import Path
import fitz  # PyMuPDF
import docx
import pandas as pd
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import mammoth
from markdownify import markdownify as md
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional

class IngestaoDeArquivos:
    """
    Classe para ingestão de arquivos (.txt, .md, .docx, .xls, .xlsx, .pdf, .json) com OCR, conversão para Markdown,
    logging configurável, processamento paralelo e filtros customizáveis.
    """

    def __init__(
        self,
        tesseract_path: str = None,
        output_path: str = None,
        log_level: int = logging.INFO,
        language: str = "pt",
        max_workers: int = 4
    ):
        # Configuração do Tesseract
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.supported_formats = ['.txt', '.md', '.docx', '.xls', '.xlsx', '.pdf', '.json']
        self.output_path = Path(output_path) if output_path else None
        if self.output_path:
            self.output_path.mkdir(parents=True, exist_ok=True)
        self.language = language
        self.max_workers = max_workers

        # Configuração de logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("IngestaoDeArquivos")

    def process_file(self, file_path: str, save_markdown: bool = False, return_format: str = "markdown", ocr_func=None, llm_func=None) -> dict:
        """
        Processa um único arquivo e retorna dicionário com nome, formato, conteúdo e metadados.
        """
        ocr_func = ocr_func or pytesseract.image_to_string
        llm_func = llm_func or self.pos_processamento_llm

        if not os.path.exists(file_path):
            self.logger.warning(f"Arquivo não encontrado: {file_path}")
            return None

        ext = Path(file_path).suffix.lower()
        if ext not in self.supported_formats:
            self.logger.warning(f"Formato não suportado: {ext}")
            return None

        try:
            if ext in ['.txt', '.md']:
                content = self._extract_txt(file_path)
                markdown = md(content)
            elif ext == '.docx':
                markdown = self._extract_docx(file_path)
            elif ext in ['.xls', '.xlsx']:
                markdown = self._extract_excel(file_path)
            elif ext == '.pdf':
                markdown = self._extract_pdf(file_path, ocr_func=ocr_func)
            elif ext == '.json':
                markdown = self._extract_json(file_path)
            else:
                return None

            # Pós-processamento LLM (stub)
            # markdown_corrigido = self.pos_processamento_llm(markdown)
            markdown_corrigido = llm_func(markdown)
            # Retorno customizável
            if return_format == "markdown":
                content_out = markdown_corrigido
            elif return_format == "text":
                content_out = self._markdown_to_text(markdown_corrigido)
            elif return_format == "html":
                content_out = self._markdown_to_html(markdown_corrigido)
            else:
                content_out = markdown_corrigido

            metadados = {
                "tamanho_bytes": os.path.getsize(file_path),
                "formato": ext[1:],
                "caminho": file_path,
                "tamanho_markdown": len(markdown_corrigido),
                "linhas_markdown": markdown_corrigido.count('\n') + 1
            }

            if save_markdown and self.output_path:
                output_file = self.output_path / (Path(file_path).stem + ".md")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(markdown_corrigido)

            return {
                "nome_arquivo": os.path.basename(file_path),
                "formato": ext[1:],
                "conteudo": content_out,
                "metadados": metadados
            }
        except Exception as e:
            self.logger.error(f"Erro ao processar {file_path}: {str(e)}")
            return None

    def process_directory(
        self,
        dir_path: str,
        save_markdown: bool = False,
        filter_ext: list = None,
        min_size: int = 0,
        return_format: str = "markdown"
    ) -> list:
        """
        Processa todos os arquivos suportados em um diretório, com filtros e processamento paralelo.
        """
        if not os.path.isdir(dir_path):
            self.logger.warning(f"Diretório não encontrado: {dir_path}")
            return []

        documentos = []
        files = [
            os.path.join(dir_path, f)
            for f in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, f))
        ]

        # Filtros
        if filter_ext:
            files = [f for f in files if Path(f).suffix.lower() in filter_ext]
        else:
            files = [f for f in files if Path(f).suffix.lower() in self.supported_formats]
        if min_size > 0:
            files = [f for f in files if os.path.getsize(f) >= min_size]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.process_file, f, save_markdown, return_format): f
                for f in files
            }
            for future in as_completed(future_to_file):
                doc = future.result()
                if doc:
                    documentos.append(doc)
        return documentos

    def _extract_txt(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin1') as f:
                    return f.read()
            except Exception as e:
                self.logger.error(f"Erro ao ler TXT {file_path} (latin1): {e}")
                return ""
        except Exception as e:
            self.logger.error(f"Erro ao ler TXT {file_path}: {e}")
            return ""

    def _extract_docx(self, file_path: str) -> str:
        try:
            with open(file_path, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file)
                return result.value
        except Exception:
            try:
                doc = docx.Document(file_path)
                return "\n\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                self.logger.error(f"Erro ao processar DOCX {file_path}: {e}")
                return ""

    def _extract_excel(self, file_path: str) -> str:
        try:
            dfs = pd.read_excel(file_path, sheet_name=None)
            markdown_parts = []
            for sheet, df in dfs.items():
                markdown_parts.append(f"## Planilha: {sheet}\n\n{df.to_markdown(index=False)}")
            return "\n\n".join(markdown_parts)
        except Exception as e:
            self.logger.error(f"Erro ao processar Excel {file_path}: {e}")
            return ""

    def _extract_pdf(self, file_path: str, ocr_func=None) -> str:
        ocr_func = ocr_func or pytesseract.image_to_string
        try:
            doc = fitz.open(file_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            if not full_text.strip():
                raise ValueError("PDF sem texto visível")
            return md(full_text)
        except Exception:
            # PDF escaneado, usar OCR
            try:
                images = convert_from_path(file_path)
                text = ""
                for img in images:
                    text += ocr_func(img, lang=self.language) + "\n\n"
                return md(text)
            except Exception as e:
                self.logger.error(f"Erro ao processar PDF (OCR) {file_path}: {e}")
                return ""

    def _extract_json(self, file_path: str) -> str:
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            import pprint
            return md(pprint.pformat(data))
        except Exception as e:
            self.logger.error(f"Erro ao processar JSON {file_path}: {e}")
            return ""

    def _markdown_to_text(self, markdown_str: str) -> str:
        import re
        text = re.sub(r'[#>*_`]', '', markdown_str)
        return text.strip()

    def _markdown_to_html(self, markdown_str: str) -> str:
        try:
            import markdown
            return markdown.markdown(markdown_str)
        except ImportError:
            self.logger.warning("Pacote 'markdown' não instalado. Retornando markdown puro.")
            return markdown_str

    def pos_processamento_llm(self, texto: str) -> str:
        """
        Pós-processamento do texto usando LLM para correção contextual.
        (Stub: substitua pela chamada real ao LLM)
        """
        return texto  # Por enquanto, retorna o texto sem alteração