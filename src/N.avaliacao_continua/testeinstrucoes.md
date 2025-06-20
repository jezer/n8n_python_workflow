# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### N.avaliacao_continua/avaliacao_continua.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `rouge_score`, `bert_score`, `logging`
  - (Opcional) LLM judge disponível (ou usar stub)

- [ ] **Entradas válidas**
  - Lista de dicts com:
    - `"query"`: string
    - `"resposta"`: string
    - (Opcional) `"referencia"`: string
  - Lista de referências (opcional, mesma ordem dos resultados)

- [ ] **Entradas inválidas**
  - Lista vazia
  - Dicts sem `"query"` ou `"resposta"`
  - Respostas ou referências vazias
  - Tipos errados (ex: string ao invés de lista de dicts)

- [ ] **Comportamentos esperados**
  - ROUGE-L e BERTScore são calculados corretamente quando referência está disponível
  - Avaliação LLM-as-a-judge retorna string (stub ou real)
  - Avaliação humana retorna stub
  - Logs informam progresso e erros
  - Retorno é lista de avaliações agregadas por item

- [ ] **Mockar (Simular) quais dependências**
  - LLM judge: pode ser substituído por stub para testes rápidos
  - ROUGE scorer e BERT scorer: podem ser substituídos por mocks para controlar saída

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Lista de resultados e referências válidas resulta em avaliações automáticas e LLM-as-a-judge corretas

- **Edge Cases (Casos extremos)**
  - Lista de resultados vazia (retorna lista vazia)
  - Item sem referência (avaliação automática vazia)
  - Dict sem `"query"` ou `"resposta"` (deve ser ignorado ou tratado)
  - Resposta ou referência vazia (deve ser tratada)

- **Failure Modes (Modos de falha)**
  - Falha ao calcular ROUGE ou BERTScore (deve ser tratada e logada)
  - Falha ao chamar LLM judge (deve ser tratada e logada)
  - Tipos de entrada errados: deve lançar erro claro
