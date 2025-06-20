# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### D.chunking_inteligente/chunking_inteligente.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `numpy`, `sentence-transformers`, `scikit-learn`, `logging`
  - Opcional: modelo de confiança mockado (deve implementar `predict_proba([chunk])`)

- [ ] **Entradas válidas**
  - Lista de dicionários com chave `"conteudo"` contendo textos com mais de 512 tokens.
  - Textos com tópicos distintos para testar clusterização.

- [ ] **Entradas inválidas**
  - Lista vazia.
  - Dicionários sem chave `"conteudo"`.
  - Textos muito curtos (menos que o tamanho da janela).
  - Tipos errados (ex: string ao invés de lista de dicionários).

- [ ] **Comportamentos esperados**
  - Textos são divididos em chunks com overlap.
  - Chunks são agrupados por similaridade semântica.
  - Cada chunk recebe score de confiança; chunks inválidos recebem tag 'REVISAR' e são logados.
  - Retorno é uma lista de documentos, cada um com chave `"chunks"` contendo lista de chunks validados.

- [ ] **Mockar (Simular) quais dependências**
  - Modelo de confiança (`confidence_model`): simular método `predict_proba` para controlar scores.
  - Embedding model: pode ser substituído por stub para testes rápidos.

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Documento longo é corretamente chunked, clusterizado e validado; chunks válidos e inválidos são identificados conforme esperado.

- **Edge Cases (Casos extremos)**
  - Documento com menos de 512 tokens (deve retornar um chunk único).
  - Documento com apenas um tópico (clusterização deve retornar um grupo).
  - Documento com muitos tópicos distintos (testar clusterização).
  - Dicionário sem chave `"conteudo"` (deve ser ignorado ou tratado).

- **Failure Modes (Modos de falha)**
  - Modelo de confiança lança exceção (deve ser tratado e logado).
  - Texto com encoding inválido (deve ser normalizado ou descartado).
  - Lista de entrada não é lista (deve lançar erro claro).
  - Falha ao carregar modelo de embedding (deve ser tratada).
