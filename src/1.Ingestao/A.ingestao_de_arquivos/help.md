# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Ponto de entrada do pipeline, chama a classe `IngestaoDeArquivos` para ingestão inicial dos dados.
- **A.ingestao_de_arquivos/ingestao.py**: Responsável por toda a lógica de ingestão, extração, conversão e pós-processamento dos arquivos.
- **A.ingestao_de_arquivos/__init__.py**: Apenas expõe a classe principal.
- **Dependências externas**:
  - Manipulação de arquivos: `os`, `pathlib.Path`
  - Leitura de formatos: `fitz` (PyMuPDF), `docx`, `pandas`, `pytesseract`, `PIL`, `pdf2image`, `mammoth`, `markdownify`, `markdown`, `json`, `pprint`
  - Processamento paralelo: `concurrent.futures`
  - Logging: `logging`
  - Tipagem: `typing`
- **Dependências internas**: Nenhuma explícita além do próprio pacote.

## 2. Descrição por Arquivo

### A.ingestao_de_arquivos/ingestao.py

- **Propósito principal**: Realizar ingestão de arquivos de múltiplos formatos, aplicando OCR, conversão para Markdown, pós-processamento (stub LLM), logging e processamento paralelo.
- **Classe exportada**: `IngestaoDeArquivos`
  - **__init__**: Configura caminhos, logging, formatos suportados, Tesseract, etc.
  - **process_file**: Processa um arquivo individual, aplica extração e pós-processamento, retorna dict com conteúdo e metadados. Permite injeção de funções de OCR e LLM para facilitar testes/mocks.
  - **process_directory**: Processa todos os arquivos suportados em um diretório, com filtros e processamento paralelo.
  - **_extract_txt/_extract_docx/_extract_excel/_extract_pdf/_extract_json**: Métodos privados para extração de conteúdo de cada formato.
  - **_markdown_to_text/_markdown_to_html**: Conversão de Markdown para outros formatos.
  - **pos_processamento_llm**: Stub para pós-processamento com LLM.
- **Destaques**:
  - Suporte a múltiplos formatos: `.txt`, `.md`, `.docx`, `.xls`, `.xlsx`, `.pdf`, `.json`
  - OCR automático para PDFs escaneados, com possibilidade de mockar a função OCR.
  - Pós-processamento LLM injetável (facilita testes).
  - Processamento paralelo com `ThreadPoolExecutor`.
  - Logging detalhado para erros e progresso.
  - Salva arquivos em Markdown se solicitado.
  - Retorno padronizado: nome, formato, conteúdo, metadados.

### A.ingestao_de_arquivos/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `IngestaoDeArquivos`
- **Dependências internas**: Importa de `.ingestao`
- **Dependências externas**: Nenhuma

## 3. Fluxo Executável

1. **main.py** é executado.
2. Recebe o caminho da pasta de entrada.
3. Instancia a classe `IngestaoDeArquivos` e executa `process_directory`, processando todos os arquivos suportados.
4. Cada arquivo é processado (OCR, extração, pós-processamento LLM, logging, etc.).
5. O resultado (lista de documentos processados) é passado para a próxima etapa do pipeline (segmentação, limpeza, etc.), conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).

## 4. Pontos de Testabilidade e Boas Práticas

- **Injeção de dependências**: O uso dos parâmetros `ocr_func` e `llm_func` em `process_file` e `_extract_pdf` permite fácil mock em testes unitários.
- **Padronização de retorno**: Todos os métodos retornam dicts padronizados com `"nome_arquivo"`, `"formato"`, `"conteudo"`, `"metadados"`.
- **Tratamento de erros**: Logging detalhado para arquivos não encontrados, formatos não suportados, erros de leitura e exceções de OCR.
- **Processamento paralelo**: Uso de `ThreadPoolExecutor` para acelerar a ingestão em diretórios grandes.
- **Conversão universal para Markdown**: Todos os formatos são convertidos para Markdown, facilitando o processamento posterior.
- **Pós-processamento LLM**: Stub pronto para integração futura com LLM real.

## 5. Sugestões de Melhorias

- **Validação de entrada**: Adicionar validação explícita para garantir que arquivos existem e são suportados antes de processar.
- **Testes unitários**: Criar mocks para OCR e LLM, e arquivos de teste pequenos para cada formato.
- **Logs de performance**: Adicionar logs de tempo de processamento por arquivo.
- **Tratamento de encoding**: Garantir robustez para arquivos com encoding incomum.
- **Documentação**: Adicionar docstrings detalhadas para cada método privado.

---