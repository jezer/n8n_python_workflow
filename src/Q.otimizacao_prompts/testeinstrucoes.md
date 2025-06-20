# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### Q.otimizacao_prompts/otimizacao_prompts.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `logging`, `random`
  - Lista de avaliações/resultados disponível (dicts com chave `"query"`)

- [ ] **Entradas válidas**
  - Lista de dicts com chave `"query"` (pergunta)
  - Parâmetro `metodo`: `"ab_test"` ou `"star"`

- [ ] **Entradas inválidas**
  - Lista vazia
  - Dicts sem chave `"query"`
  - Parâmetro `metodo` inválido
  - Tipos errados (ex: string ao invés de lista de dicts)

- [ ] **Comportamentos esperados**
  - Para cada pergunta, executa otimização de prompts (A/B test ou STaR)
  - Loga templates, prompts, respostas e scores
  - Retorna lista de melhores templates/prompts e scores
  - Lança erro para método não suportado

- [ ] **Mockar (Simular) quais dependências**
  - Cliente LLM: pode ser substituído por stub para testes rápidos
  - Avaliador: pode ser substituído por stub para controlar scores

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Lista de perguntas válidas resulta em otimização e seleção do melhor template/prompt para cada uma

- **Edge Cases (Casos extremos)**
  - Lista de perguntas vazia (retorna lista vazia)
  - Dict sem `"query"` (deve ser ignorado ou tratado)
  - Parâmetro `metodo` inválido (deve lançar ValueError)
  - Templates customizados (testar com lista diferente)

- **Failure Modes (Modos de falha)**
  - Falha ao chamar LLM ou avaliador (deve ser tratada e logada)
  - Tipos de entrada errados: deve lançar erro claro
