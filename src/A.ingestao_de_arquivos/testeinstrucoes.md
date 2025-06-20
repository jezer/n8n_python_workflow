# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### A.ingestao_de_arquivos/ingestao.py

- [ ] **Pré-condições para teste**
  - Diretório com arquivos de texto/imagem de formatos suportados.
  - Dependências instaladas: Tesseract, PyMuPDF, pandas, PIL, pdf2image, mammoth, markdownify, markdown, etc.
  - Permissões de leitura/escrita nos diretórios de entrada/saída.

- [ ] **Entradas válidas**
  - Caminho para diretório com arquivos `.txt`, `.md`, `.docx`, `.xls`, `.xlsx`, `.pdf`, `.json`.

- [ ] **Entradas inválidas**
  - Diretório inexistente.
  - Arquivos corrompidos ou com formato não suportado.
  - Arquivos vazios.

- [ ] **Comportamentos esperados**
  - Retorna lista de documentos processados com conteúdo e metadados.
  - Logs de erros para arquivos inválidos ou não suportados.
  - Arquivos processados são salvos em Markdown se solicitado.

- [ ] **Mockar (Simular) quais dependências**
  - OCR (Tesseract): pode ser mockado para acelerar testes.
  - Chamadas LLM (stub).
  - Leitura de arquivos (usar arquivos pequenos ou mocks).

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Diretório com arquivos válidos de vários formatos resulta em lista de documentos processados corretamente.

- **Edge Cases (Casos extremos)**
  - Diretório vazio (retorna lista vazia).
  - Arquivo muito grande (testar performance e logs).
  - Arquivo com caracteres especiais ou encoding incomum.

- **Failure Modes (Modos de falha)**
  - Falha de conexão com Tesseract/OCR.
  - Erro ao ler arquivo corrompido.
  - Exceções não tratadas durante processamento.