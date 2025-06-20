# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Ponto de entrada do pipeline, chama a etapa de classificação/tagging após chunking inteligente.
- **E.classificacao_tagging/__init__.py**: Expõe a classe principal `ClassificacaoTagging` do módulo `classificacao_tagging.py`.
- **E.classificacao_tagging/classificacao_tagging.py**:
  - **Dependências externas**:
    - `logging`: para instrumentação e logs.
    - `typing`: tipagem estática.
    - (Opcional) Modelo de classificação multi-label (ex: DeBERTa-v3 fine-tuned).
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.

- **Fluxo de dados**:
  - Recebe documentos chunked da etapa anterior (D).
  - Processa cada chunk, atribuindo tags multi-label e marcando chunks para revisão se necessário.
  - Retorna documentos com lista de chunks classificados para a próxima etapa (F).

---

## 2. Descrição por Arquivo

### E.classificacao_tagging/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `ClassificacaoTagging`
- **Dependências internas**: Importa de `.classificacao_tagging`
- **Dependências externas**: Nenhuma

### E.classificacao_tagging/classificacao_tagging.py

- **Propósito principal**: Implementa classificação multi-label de chunks usando modelo fine-tuned (ex: DeBERTa-v3). Chunks com score < 0.7 recebem tag 'REVISAR'.
- **Classe exportada**: `ClassificacaoTagging`
  - **__init__**: 
    - Parâmetros configuráveis: modelo de classificação, lista de labels, threshold, nível de log.
    - Instancia modelo ou usa stub para testes.
  - **_stub_model**:
    - Gera scores aleatórios para cada label (usado como fallback/mocking).
  - **classificar_chunk**:
    - Classifica um chunk, atribui tags e marca para revisão se necessário.
    - Loga chunks marcados para revisão.
  - **run**:
    - Pipeline principal: recebe lista de documentos (cada doc com 'chunks'), aplica classificação em cada chunk e retorna documentos com chunks classificados.
- **Dependências externas**: `logging`, `typing`, (opcional) modelo de classificação.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando documentos chunked para a etapa de classificação/tagging.
2. Instancia-se `ClassificacaoTagging` (com ou sem modelo de classificação).
3. Chama-se o método `run(documentos)`:
   - Para cada documento:
     - Para cada chunk:
       - Classifica usando o modelo.
       - Atribui tags com score >= threshold.
       - Se algum score < threshold, adiciona tag 'REVISAR' e loga.
     - Adiciona lista de chunks classificados ao documento.
   - Retorna lista de documentos enriquecidos com chunks classificados.
4. Os documentos classificados seguem para a etapa de grafo de conhecimento.
