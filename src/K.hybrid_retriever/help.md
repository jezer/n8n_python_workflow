# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando o módulo `K.hybrid_retriever` na etapa de busca híbrida, conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).
- **K.hybrid_retriever/__init__.py**: Expõe a classe principal `HybridRetriever` do módulo `hybrid_retriever.py`.
- **K.hybrid_retriever/hybrid_retriever.py**:
  - **Dependências externas**:
    - `numpy`: manipulação de arrays numéricos.
    - `faiss`: indexação e busca vetorial.
    - `rank_bm25`: recuperação esparsa (BM25).
    - `transformers`: modelos de embeddings densos e tokenização.
    - `sentence_transformers`: cross-encoder para reranking.
    - `logging`, `datetime`, `timedelta`: instrumentação, cache e logs.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.

- **Fluxo de dados**:
  - Recebe consulta e lista de documentos.
  - Calcula embeddings densos e scores esparsos (BM25).
  - Combina scores com pesos configuráveis.
  - Aplica reranking com cross-encoder.
  - Fallback para BM25 puro em caso de erro.

---

## 2. Descrição por Arquivo

### K.hybrid_retriever/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `HybridRetriever`
- **Dependências internas**: Importa de `.hybrid_retriever`
- **Dependências externas**: Nenhuma

### K.hybrid_retriever/hybrid_retriever.py

- **Propósito principal**: Implementa busca híbrida combinando recuperação densa (embeddings), esparsa (BM25) e reranking (cross-encoder), com cache de embeddings e fallback robusto.
- **Classe exportada**: `HybridRetriever`
  - **__init__**: 
    - Parâmetros: nomes dos modelos, pesos dos scores, TTL do cache, threshold de similaridade.
    - Instancia modelos, tokenizadores, cross-encoder e logger.
  - **_initialize_models**:
    - Carrega modelos e tokenizadores necessários.
  - **_get_embedding**:
    - Gera embedding denso para texto, com cache e TTL.
  - **_mean_pooling**:
    - Pooling para gerar embedding de frase a partir de tokens.
  - **_sparse_retrieval**:
    - Recuperação esparsa usando BM25.
  - **_dense_retrieval**:
    - Recuperação densa via similaridade de cosseno.
  - **retrieve**:
    - Método principal: executa busca híbrida, combina scores, aplica reranking e fallback.
  - **_rerank**:
    - Reranking dos resultados usando cross-encoder.
  - **_fallback_retrieval**:
    - Fallback para BM25 puro em caso de erro.
- **Dependências externas**: `numpy`, `faiss`, `rank_bm25`, `transformers`, `sentence_transformers`, `logging`, `datetime`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando consulta e documentos para o `HybridRetriever`.
2. Instancia-se `HybridRetriever` (com modelos e pesos desejados).
3. Chama-se o método `retrieve(query, documents, k, use_reranking)`:
   - Pré-computa embeddings densos dos documentos.
   - Executa recuperação esparsa (BM25) e densa (similaridade de cosseno).
   - Combina scores com pesos configuráveis.
   - Seleciona top-k resultados.
   - Aplica reranking com cross-encoder se solicitado.
   - Em caso de erro, faz fallback para BM25 puro.
   - Retorna lista de tuplas (índice, score, texto do documento).
4. Resultados são usados na etapa de reranking e passagem para LLM com RAG.
