# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### E.classificacao_tagging/classificacao_tagging.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `logging`
  - Opcional: modelo de classificação mockado (deve implementar método `__call__` ou `predict_proba(texto)`)

- [ ] **Entradas válidas**
  - Lista de dicionários com chave `"chunks"` contendo lista de strings ou dicionários com chave `"chunk"`.

- [ ] **Entradas inválidas**
  - Lista vazia.
  - Dicionários sem chave `"chunks"`.
  - Chunks vazios ou não textuais.
  - Tipos errados (ex: string ao invés de lista de dicionários).

- [ ] **Comportamentos esperados**
  - Cada chunk recebe tags multi-label conforme scores do modelo.
  - Chunks com algum score < threshold recebem tag 'REVISAR' e são logados.
  - Retorno é uma lista de documentos, cada um com chave `"chunks_classificados"` contendo lista de resultados.

- [ ] **Mockar (Simular) quais dependências**
  - Modelo de classificação: simular método `__call__` ou `predict_proba` para controlar scores e tags.

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Documento com vários chunks é corretamente classificado; tags e revisão atribuídas conforme esperado.

- **Edge Cases (Casos extremos)**
  - Documento sem chunks (deve ser ignorado ou tratado).
  - Chunk com todos scores acima do threshold (não recebe 'REVISAR').
  - Chunk com todos scores abaixo do threshold (recebe apenas 'REVISAR').
  - Dicionário sem chave `"chunks"` (deve ser ignorado ou tratado).

- **Failure Modes (Modos de falha)**
  - Modelo de classificação lança exceção (deve ser tratado e logado).
  - Chunk não textual (deve ser descartado ou tratado).
  - Lista de entrada não é lista (deve lançar erro claro).