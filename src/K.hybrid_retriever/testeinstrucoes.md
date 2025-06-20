# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### K.hybrid_retriever/hybrid_retriever.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `numpy`, `faiss`, `rank_bm25`, `transformers`, `sentence_transformers`, `logging`
  - Modelos necessários disponíveis localmente ou via internet

- [ ] **Entradas válidas**
  - Consulta (`query`) como string
  - Lista de documentos (`documents`) como lista de strings
  - Parâmetros opcionais: `k` (int), `use_reranking` (bool)

- [ ] **Entradas inválidas**
  - Lista de documentos vazia
  - Consulta vazia ou não textual
  - Documentos não textuais
  - Tipos errados (ex: string ao invés de lista de strings)

- [ ] **Comportamentos esperados**
  - Embeddings são gerados e cacheados corretamente
  - Recuperação esparsa e densa retornam índices e scores esperados
  - Scores são combinados conforme pesos
  - Reranking é aplicado corretamente (quando solicitado)
  - Fallback para BM25 puro em caso de erro
  - Logs informam progresso, erros e uso de fallback

- [ ] **Mockar (Simular) quais dependências**
  - Modelos de embedding e cross-encoder: podem ser substituídos por stubs para testes rápidos
  - BM25: pode ser simulado para controlar scores
  - Sistema de arquivos/modelos: pode ser simulado para testar fallback

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Consulta e documentos válidos resultam em busca híbrida, reranking e retorno dos top-k esperados

- **Edge Cases (Casos extremos)**
  - Lista de documentos vazia (retorna lista vazia)
  - Consulta vazia (deve ser tratada ou retornar lista vazia)
  - Documentos idênticos (verificar desempate)
  - Documentos muito longos (testar truncamento/tokenização)

- **Failure Modes (Modos de falha)**
  - Falha ao carregar modelo (deve ser tratada e logada)
  - Falha ao gerar embedding (deve ser tratada e logada)
  - Falha no cross-encoder (reranking): deve retornar ordem original
  - Falha geral: fallback para BM25 puro
  - Tipos de entrada errados: deve lançar erro claro
