# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando cada etapa conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).
- **P.atualizacao_incremental/__init__.py**: Expõe a classe principal `AtualizacaoIncremental` do módulo `atualizacao_incremental.py`.
- **P.atualizacao_incremental/atualizacao_incremental.py**:
  - **Dependências externas**:
    - `numpy`: manipulação de arrays numéricos.
    - `os`: manipulação de arquivos e diretórios.
    - `logging`: instrumentação e logs.
    - `faiss`: busca vetorial para cálculo de recall.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.
- **Fluxo de dados**:
  - Recebe embeddings antigos, novos dados, consultas e ground-truth.
  - Realiza atualização incremental dos embeddings (delta-tuning).
  - Versiona embeddings e salva em disco.
  - Avalia recall@k antes e depois da atualização.
  - Executa rollback automático se recall cair mais que 5%.

---

## 2. Descrição por Arquivo

### P.atualizacao_incremental/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `AtualizacaoIncremental`
- **Dependências internas**: Importa de `.atualizacao_incremental`
- **Dependências externas**: Nenhuma

### P.atualizacao_incremental/atualizacao_incremental.py

- **Propósito principal**: Implementa atualização incremental de embeddings (delta-tuning), versionamento, avaliação de recall e rollback automático.
- **Classe exportada**: `AtualizacaoIncremental`
  - **__init__**: 
    - Parâmetros: caminho dos embeddings, threshold de recall, nível de log.
    - Cria diretório de versões e logger.
  - **salvar_embeddings**:
    - Salva embeddings numpy em arquivo versionado.
  - **carregar_embeddings**:
    - Carrega embeddings de arquivo versionado.
  - **delta_tuning**:
    - Atualiza embeddings antigos com novos dados (concatenação e normalização).
  - **avaliar_recall**:
    - Calcula recall@k usando FAISS.
  - **rollback**:
    - Loga rollback automático para versão anterior.
  - **run**:
    - Orquestra atualização incremental, avaliação de recall e rollback se necessário.
    - Retorna status e métricas de recall.
- **Dependências externas**: `numpy`, `os`, `logging`, `faiss`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando embeddings antigos, novos dados, consultas e ground-truth para o `AtualizacaoIncremental`.
2. Instancia-se `AtualizacaoIncremental` (com caminho, threshold e log desejados).
3. Chama-se o método `run(...)`:
   - Realiza delta-tuning dos embeddings.
   - Salva embeddings atualizados em disco (versionamento).
   - Avalia recall@k dos embeddings antigos e atualizados.
   - Se recall cair mais que 5%, executa rollback automático e retorna status "rollback".
   - Caso contrário, retorna status "atualizado" e métricas de recall.
4. Resultados podem ser usados para monitoramento, auditoria e controle de versões dos embeddings.
