# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Ponto de entrada do pipeline, chama a etapa de chunking inteligente após limpeza e normalização.
- **D.chunking_inteligente/__init__.py**: Expõe a classe principal `ChunkingInteligente` do módulo `chunking_inteligente.py`.
- **D.chunking_inteligente/chunking_inteligente.py**:
  - **Dependências externas**:
    - `numpy` (np): manipulação de arrays.
    - `sentence_transformers.SentenceTransformer`: geração de embeddings semânticos.
    - `sklearn.cluster.AgglomerativeClustering`: clusterização dos chunks.
    - `logging`: instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.

- **Fluxo de dados**:
  - Recebe documentos limpos da etapa anterior (C).
  - Processa cada documento, gerando chunks semânticos validados.
  - Retorna documentos com lista de chunks validados para a próxima etapa (E).

---

## 2. Descrição por Arquivo

### D.chunking_inteligente/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `ChunkingInteligente`
- **Dependências internas**: Importa de `.chunking_inteligente`
- **Dependências externas**: Nenhuma

### D.chunking_inteligente/chunking_inteligente.py

- **Propósito principal**: Implementa chunking semântico com janela deslizante, overlap, clusterização por embeddings e validação de confiança.
- **Classe exportada**: `ChunkingInteligente`
  - **__init__**: 
    - Parâmetros configuráveis: modelo de embedding, tamanho da janela, overlap, modelo de confiança, nível de log.
    - Instancia modelos necessários.
  - **_split_sliding_window**:
    - Divide texto em chunks com janela deslizante e overlap.
  - **_cluster_chunks**:
    - Gera embeddings dos chunks e agrupa por tópicos naturais via clusterização.
  - **_validar_chunks**:
    - Valida cada chunk usando modelo de confiança (se fornecido); chunks com score < 0.7 recebem tag 'REVISAR' e são logados.
  - **run**:
    - Pipeline principal: recebe lista de documentos, aplica chunking, clusterização, validação e retorna documentos com chunks validados.
- **Dependências externas**: `numpy`, `sentence_transformers`, `sklearn`, `logging`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando documentos limpos para a etapa de chunking inteligente.
2. Instancia-se `ChunkingInteligente` (com ou sem modelo de confiança).
3. Chama-se o método `run(documentos)`:
   - Para cada documento:
     - Divide o texto em chunks com janela deslizante e overlap.
     - Gera embeddings dos chunks e agrupa por tópicos naturais via clusterização.
     - Ajusta tamanho dos chunks para manter contexto (concatena grupos).
     - Valida cada chunk (score de confiança); chunks inválidos recebem tag 'REVISAR' e são logados.
     - Adiciona lista de chunks validados ao documento.
   - Retorna lista de documentos enriquecidos com chunks validados.
4. Os documentos chunked seguem para a etapa de classificação/tagging.

---
