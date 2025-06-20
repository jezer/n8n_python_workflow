# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### F.grafo_conhecimento/grafo_conhecimento.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `rdflib`, `logging`
  - Documentos de entrada devem conter chave `"chunks_classificados"` (lista de strings ou dicionários com `"chunk"`)

- [ ] **Entradas válidas**
  - Lista de dicionários com chave `"chunks_classificados"` contendo textos com padrões reconhecíveis (ex: "X é um Y").
  - Chunks com diferentes entidades e predicados.

- [ ] **Entradas inválidas**
  - Lista vazia.
  - Dicionários sem chave `"chunks_classificados"`.
  - Chunks vazios ou não textuais.
  - Tipos errados (ex: string ao invés de lista de dicionários).

- [ ] **Comportamentos esperados**
  - Triplas são extraídas corretamente dos chunks.
  - Entidades são normalizadas conforme regras.
  - Triplas são adicionadas ao grafo RDF.
  - Logs informam o número de triplas geradas.
  - Exportação do grafo gera arquivo RDF válido.

- [ ] **Mockar (Simular) quais dependências**
  - Função de extração de triplas (pode ser substituída por stub para controlar saída).
  - Função de normalização de entidades.

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Documento com vários chunks contendo frases no padrão "X é um Y" resulta em múltiplas triplas no grafo.

- **Edge Cases (Casos extremos)**
  - Documento sem chunks (deve ser ignorado ou tratado).
  - Chunk sem padrão reconhecível (não gera triplas).
  - Chunk com entidades que precisam de normalização (ex: "Python3" → "Python 3").
  - Dicionário sem chave `"chunks_classificados"` (deve ser ignorado ou tratado).

- **Failure Modes (Modos de falha)**
  - Falha ao adicionar tripla inválida (deve ser tratada e logada).
  - Lista de entrada não é lista (deve lançar erro claro).
  - Falha ao exportar grafo (deve ser tratada e logada).
