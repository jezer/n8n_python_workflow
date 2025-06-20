# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### O.retriever_adaptativo/retriever_adaptativo.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `logging`
  - Avaliações disponíveis (lista de dicts com métricas automáticas)

- [ ] **Entradas válidas**
  - Lista de dicts com chave `"avaliacao_automatica"` contendo `"rougeL"` e/ou `"bertscore_F1"`
  - Lista de exemplos positivos (opcional)

- [ ] **Entradas inválidas**
  - Lista vazia
  - Dicts sem chave `"avaliacao_automatica"`
  - Métricas ausentes ou valores não numéricos
  - Tipos errados (ex: string ao invés de lista de dicts)

- [ ] **Comportamentos esperados**
  - Hard negatives são identificados corretamente com base nos thresholds
  - Fine-tuning é chamado (stub) e logado
  - Logs informam número de hard negatives e progresso do fine-tuning
  - Retorno é um dict com hard negatives e resultado do fine-tuning

- [ ] **Mockar (Simular) quais dependências**
  - Modelo do retriever: pode ser substituído por stub para testes rápidos

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Lista de avaliações com métricas variadas resulta em identificação correta de hard negatives e chamada do fine-tuning

- **Edge Cases (Casos extremos)**
  - Lista de avaliações vazia (retorna hard negatives vazio)
  - Todas as avaliações acima dos thresholds (nenhum hard negative)
  - Dicts sem `"avaliacao_automatica"` (devem ser ignorados ou tratados)
  - Métricas ausentes ou não numéricas (devem ser tratadas)

- **Failure Modes (Modos de falha)**
  - Falha ao acessar métricas (deve ser tratada e logada)
  - Falha ao chamar fine-tuning (deve ser tratada e logada)
  - Tipos de entrada errados: deve lançar erro claro
