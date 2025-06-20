# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando o módulo `L.reranking_cross_encoder` na etapa de reranking após a busca híbrida (`K.hybrid_retriever`), conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).
- **L.reranking_cross_encoder/__init__.py**: Expõe a classe principal `RerankingCrossEncoder` do módulo `reranking_cross_encoder.py`.
- **L.reranking_cross_encoder/reranking_cross_encoder.py**:
  - **Dependências externas**:
    - `sentence_transformers.CrossEncoder`: modelo de reranking.
    - `numpy`: manipulação de arrays numéricos.
    - `logging`: instrumentação e logs.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.
  - **Integração**: Espera receber resultados do retriever híbrido (com scores dense/sparse) e retorna lista reranqueada.

---

## 2. Descrição por Arquivo

### L.reranking_cross_encoder/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `RerankingCrossEncoder`
- **Dependências internas**: Importa de `.reranking_cross_encoder`
- **Dependências externas**: Nenhuma

### L.reranking_cross_encoder/reranking_cross_encoder.py

- **Propósito principal**: Implementa reranking de resultados de busca usando cross-encoder, combinando scores dense/sparse e calibrando pesos via grid search.
- **Classe exportada**: `RerankingCrossEncoder`
  - **__init__**: 
    - Parâmetros: nome do modelo cross-encoder, pesos dense/sparse, grid search, nível de log.
    - Instancia cross-encoder e logger.
  - **calibrar_pesos**:
    - Calibra pesos dense/sparse via grid search para maximizar métrica (stub: score aleatório).
  - **combinar_scores**:
    - Combina scores dense/sparse conforme pesos.
  - **rerank**:
    - Recebe query e docs (com scores), aplica cross-encoder e retorna docs reranqueados pelo score final.
  - **run**:
    - Recebe lista de dicts com 'query' e 'resultados', aplica rerank em cada grupo.
- **Dependências externas**: `sentence_transformers`, `numpy`, `logging`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando resultados do retriever híbrido para o `RerankingCrossEncoder`.
2. Instancia-se `RerankingCrossEncoder` (com modelo e pesos desejados).
3. Chama-se o método `run(resultados_retriever)`:
   - Para cada item (query + docs):
     - Aplica `rerank` para combinar scores dense/sparse e cross-encoder.
     - Ordena docs pelo score final.
   - Retorna lista de queries com docs reranqueados.
4. Resultados são usados na etapa de passagem para LLM com RAG.
