# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### M.llm_com_rag/llm_com_rag.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `sentence-transformers`, `numpy`, `logging`
  - Cliente LLM disponível (ou usar stub)

- [ ] **Entradas válidas**
  - Lista de dicts com:
    - `"query"`: string
    - `"resultados"`: lista de docs relevantes (cada doc pode ser tupla/lista ou string)

- [ ] **Entradas inválidas**
  - Lista vazia
  - Dicts sem `"query"` ou `"resultados"`
  - Docs não textuais ou malformados
  - Tipos errados (ex: string ao invés de lista de dicts)

- [ ] **Comportamentos esperados**
  - Seleção dos top-3 exemplos few-shot mais similares à query via embeddings
  - Fallback para exemplos genéricos se similaridade < threshold
  - Prompt é montado corretamente com exemplos, contexto e query
  - Resposta é gerada pelo LLM (ou stub)
  - Logs informam seleção de exemplos, geração de resposta e uso de fallback

- [ ] **Mockar (Simular) quais dependências**
  - Cliente LLM: pode ser substituído por stub para testes rápidos
  - Modelo de embedding: pode ser substituído por stub para acelerar testes

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Lista de queries e docs válidos resulta em prompts corretos e respostas geradas

- **Edge Cases (Casos extremos)**
  - Lista de docs vazia (prompt sem contexto, mas resposta gerada)
  - Query sem similaridade com exemplos (usa fallback)
  - Dict sem `"query"` ou `"resultados"` (deve ser ignorado ou tratado)
  - Docs malformados (deve ser tratados ou logados)

- **Failure Modes (Modos de falha)**
  - Falha ao gerar embedding (deve ser tratada e logada)
  - Falha ao chamar LLM (deve ser tratada e logada)
  - Tipos de entrada errados: deve lançar erro claro
