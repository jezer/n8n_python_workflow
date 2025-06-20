# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### H.embeddings_especializados/embeddings_especializados.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `sentence-transformers`, `logging`
  - Modelos de embedding disponíveis localmente ou via internet

- [ ] **Entradas válidas**
  - Lista de dicionários com chaves `"pergunta_gerada"` e `"resposta_gerada"` (QAs).

- [ ] **Entradas inválidas**
  - Lista vazia.
  - Dicionários sem as chaves esperadas.
  - Textos muito curtos ou vazios.
  - Tipos errados (ex: string ao invés de lista de dicionários).

- [ ] **Comportamentos esperados**
  - Embeddings são gerados para cada QA usando o modelo especificado.
  - Embeddings são adicionados ao dicionário de cada QA na chave `"embedding"`.
  - Logs informam o modelo utilizado e progresso.
  - Métodos de fine-tune e monitoramento apenas logam mensagem (stub).

- [ ] **Mockar (Simular) quais dependências**
  - Modelo de embedding (`SentenceTransformer`): pode ser substituído por stub para testes rápidos.
  - Métodos de fine-tune e monitoramento: não precisam de mock, pois são stubs.

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Lista de QAs bem formatados resulta em embeddings gerados e adicionados corretamente.

- **Edge Cases (Casos extremos)**
  - Lista de QAs vazia (retorna lista vazia).
  - QA com campos vazios ou nulos (embedding gerado para string vazia ou tratado).
  - Dicionário sem as chaves esperadas (deve ser ignorado ou tratado).

- **Failure Modes (Modos de falha)**
  - Falha ao carregar modelo de embedding (deve ser tratada e logada).
  - Lista de entrada não é lista (deve lançar erro claro).
  - Falha ao gerar embedding (deve ser tratada e logada).
