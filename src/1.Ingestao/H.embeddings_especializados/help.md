# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando cada etapa conforme o fluxo do arquivo [`fluxo.mmd`](../docs/fluxo.mmd).
- **H.embeddings_especializados/__init__.py**: Expõe a classe principal `EmbeddingsEspecializados` do módulo `embeddings_especializados.py`.
- **H.embeddings_especializados/embeddings_especializados.py**:
  - **Dependências externas**:
    - `sentence_transformers.SentenceTransformer`: geração de embeddings.
    - `logging`: instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.
- **Fluxo de dados**:
  - Recebe lista de QAs (perguntas e respostas) da etapa anterior (G).
  - Gera embeddings para cada QA usando modelos pré-treinados ou fine-tuned.
  - Permite fine-tune supervisionado (stub) e monitoramento de loss (stub).
  - Retorna QAs enriquecidos com embeddings para etapas seguintes (I).

---

## 2. Descrição por Arquivo

### H.embeddings_especializados/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `EmbeddingsEspecializados`
- **Dependências internas**: Importa de `.embeddings_especializados`
- **Dependências externas**: Nenhuma

### H.embeddings_especializados/embeddings_especializados.py

- **Propósito principal**: Implementa geração e fine-tune de embeddings especializados para QAs do domínio.
- **Classe exportada**: `EmbeddingsEspecializados`
  - **__init__**: 
    - Parâmetros: lista de modelos, modelo fine-tuned, nível de log.
    - Instancia modelos de embedding e logger.
  - **gerar_embeddings**:
    - Gera embeddings para uma lista de textos usando o modelo especificado.
  - **fine_tune**:
    - Stub para fine-tune supervisionado dos embeddings (não implementado).
  - **monitorar_loss**:
    - Stub para monitoramento do loss em dataset de validação (não implementado).
  - **run**:
    - Recebe lista de QAs, gera embeddings e adiciona ao dicionário de cada QA.
- **Dependências externas**: `sentence_transformers`, `logging`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando QAs gerados para a etapa de embeddings especializados.
2. Instancia-se `EmbeddingsEspecializados` (com ou sem modelo fine-tuned).
3. Chama-se o método `run(qas)`:
   - Para cada QA, concatena pergunta e resposta.
   - Gera embeddings usando o modelo selecionado.
   - Adiciona o embedding ao dicionário de cada QA.
   - Retorna lista de QAs enriquecidos com embeddings.
4. Os QAs com embeddings seguem para a etapa de indexação vetorial (I).
