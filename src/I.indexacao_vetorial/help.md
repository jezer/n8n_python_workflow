# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando cada etapa conforme o fluxo do arquivo [`fluxo.mmd`](../docs/fluxo.mmd).
- **H.embeddings_especializados**: Fornece embeddings para a etapa de indexação vetorial.
- **I.indexacao_vetorial/__init__.py**: Expõe a classe principal `IndexacaoVetorial` do módulo `indexacao_vetorial.py`.
- **I.indexacao_vetorial/indexacao_vetorial.py**:
  - **Dependências externas**:
    - `faiss`: indexação vetorial eficiente.
    - `numpy`: manipulação de arrays numéricos.
    - `os`: manipulação de arquivos e diretórios.
    - `logging`: instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.

- **Fluxo de dados**:
  - Recebe lista de embeddings (normalmente de QAs enriquecidos) da etapa anterior (H).
  - Constrói índice vetorial FAISS (HNSW ou IVF-PQ).
  - Permite versionamento, salvamento, carregamento e busca no índice.
  - Oferece monitoramento de recall@k para avaliação contínua.

---

## 2. Descrição por Arquivo

### I.indexacao_vetorial/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `IndexacaoVetorial`
- **Dependências internas**: Importa de `.indexacao_vetorial`
- **Dependências externas**: Nenhuma

### I.indexacao_vetorial/indexacao_vetorial.py

- **Propósito principal**: Implementa indexação vetorial usando FAISS, com suporte a métodos HNSW e IVF-PQ, versionamento de índices e monitoramento de recall.
- **Classe exportada**: `IndexacaoVetorial`
  - **__init__**: 
    - Parâmetros: método de indexação, dimensão dos vetores, caminho para salvar índices, versionamento, nível de log.
    - Instancia logger e prepara diretório.
  - **construir_indice**:
    - Cria índice FAISS (HNSW ou IVF-PQ) e adiciona embeddings.
  - **salvar_indice**:
    - Salva índice FAISS em disco, com suporte a versionamento.
  - **carregar_indice**:
    - Carrega índice FAISS de disco, com suporte a versionamento.
  - **buscar**:
    - Realiza busca vetorial (top-k) no índice carregado.
  - **monitorar_recall**:
    - Calcula recall@k para consultas e ground-truth fornecidos.
  - **run**:
    - Pipeline principal: recebe lista de dicts com 'embedding', constrói e salva índice.
- **Dependências externas**: `faiss`, `numpy`, `os`, `logging`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando QAs com embeddings para a etapa de indexação vetorial.
2. Instancia-se `IndexacaoVetorial` (com método, dimensão e versionamento desejados).
3. Chama-se o método `run(dados, versao)`:
   - Extrai embeddings dos dados.
   - Constrói índice FAISS (HNSW ou IVF-PQ).
   - Salva índice em disco, versionando se necessário.
4. O índice pode ser carregado posteriormente para buscas rápidas ou monitoramento de recall.
5. Resultados de busca e métricas de recall podem ser usados para avaliação contínua e etapas seguintes do pipeline.
