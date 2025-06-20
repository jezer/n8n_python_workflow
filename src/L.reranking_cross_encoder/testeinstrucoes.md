# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### L.reranking_cross_encoder/reranking_cross_encoder.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `sentence-transformers`, `numpy`, `logging`
  - Modelo cross-encoder disponível localmente ou via internet

- [ ] **Entradas válidas**
  - Lista de dicts com:
    - `"query"`: string
    - `"resultados"`: lista de docs, cada doc com `"dense_score"`, `"sparse_score"`, `"texto"`

- [ ] **Entradas inválidas**
  - Lista vazia
  - Dicts sem `"query"` ou `"resultados"`
  - Docs sem os campos esperados
  - Tipos errados (ex: string ao invés de lista de dicts)

- [ ] **Comportamentos esperados**
  - Cross-encoder gera scores para cada par query-doc
  - Score final é combinação ponderada dos scores dense/sparse e cross-encoder
  - Docs são ordenados pelo score final
  - Logs informam pesos, progresso e erros

- [ ] **Mockar (Simular) quais dependências**
  - Cross-encoder: pode ser substituído por stub para testes rápidos

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Lista de queries e docs válidos resulta em reranking e ordenação correta

- **Edge Cases (Casos extremos)**
  - Lista de docs vazia (retorna lista vazia)
  - Docs com scores nulos ou ausentes (deve ser tratado)
  - Dict sem `"query"` ou `"resultados"` (deve ser ignorado ou tratado)

- **Failure Modes (Modos de falha)**
  - Falha ao carregar modelo cross-encoder (deve ser tratada e logada)
  - Falha ao gerar score (deve ser tratada e logada)
  - Tipos de entrada errados: deve lançar erro claro
