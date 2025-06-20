# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### G.geracao_qa/geracao_qa.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `logging`
  - Opcional: cliente LLM mockado (deve implementar método `generate(prompt)` ou ser chamável)

- [ ] **Entradas válidas**
  - Grafo (ex: rdflib.Graph) com triplas no formato (sujeito, predicado, objeto).

- [ ] **Entradas inválidas**
  - Grafo vazio.
  - Grafo com triplas incompletas ou tipos inesperados.
  - Objeto que não implementa interface de grafo iterável.

- [ ] **Comportamentos esperados**
  - Triplas são extraídas corretamente do grafo.
  - Para cada tripla, é montado prompt few-shot e gerada pergunta e resposta.
  - Limite de perguntas respeitado (`max_pergunta`).
  - Logs informam geração de QA.
  - Retorno é uma lista de dicionários com tripla, pergunta e resposta.

- [ ] **Mockar (Simular) quais dependências**
  - Cliente LLM: simular método `generate` ou função chamável para controlar respostas.

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Grafo com várias triplas resulta em geração de QAs conforme esperado, respeitando o limite.

- **Edge Cases (Casos extremos)**
  - Grafo vazio (retorna lista vazia).
  - Tripla com campos vazios ou nulos (deve ser tratada ou ignorada).
  - Cliente LLM retorna resposta vazia ou erro (deve ser tratado e logado).

- **Failure Modes (Modos de falha)**
  - Cliente LLM lança exceção (deve ser tratado e logado).
  - Grafo não iterável (deve lançar erro claro).
  - Prompt malformado (deve ser tratado).
