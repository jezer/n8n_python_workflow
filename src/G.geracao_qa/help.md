# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Ponto de entrada do pipeline, orquestra as etapas do fluxo definido em `fluxo.mmd`.
- **F.grafo_conhecimento**: Fornece o grafo de conhecimento (rdflib.Graph) para a etapa de geração de QA.
- **G.geracao_qa/__init__.py**: Expõe a classe principal `GeracaoQA` do módulo `geracao_qa.py`.
- **G.geracao_qa/geracao_qa.py**:
  - **Dependências externas**:
    - `logging`: para instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.
  - **Dependências opcionais**: Cliente LLM (ex: GPT-4) para geração de respostas.

- **Fluxo de dados**:
  - Recebe grafo de conhecimento da etapa anterior (F).
  - Extrai triplas do grafo.
  - Para cada tripla, monta prompt few-shot e gera pergunta e resposta usando LLM.
  - Retorna lista de QAs para etapas seguintes (ex: embeddings, avaliação).

---

## 2. Descrição por Arquivo

### G.geracao_qa/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `GeracaoQA`
- **Dependências internas**: Importa de `.geracao_qa`
- **Dependências externas**: Nenhuma

### G.geracao_qa/geracao_qa.py

- **Propósito principal**: Implementa geração de perguntas e respostas (QA) a partir de triplas do grafo de conhecimento, usando prompting few-shot e chain-of-thought com LLM.
- **Classe exportada**: `GeracaoQA`
  - **__init__**: 
    - Parâmetros: cliente LLM (opcional), exemplos few-shot, máximo de perguntas, nível de log.
    - Instancia logger e define exemplos de prompt.
  - **_stub_llm**:
    - Função stub para simular resposta do LLM em ambiente de teste.
  - **montar_prompt**:
    - Monta prompt few-shot com exemplos e chain-of-thought para uma tripla.
  - **gerar_qa_para_tripla**:
    - Gera pergunta e resposta para uma tripla usando o LLM.
  - **run**:
    - Pipeline principal: recebe grafo (rdflib.Graph), extrai triplas, gera QA para até `max_pergunta` triplas, retorna lista de QAs.
- **Dependências externas**: `logging`, `typing`

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando o grafo de conhecimento para a etapa de geração de QA.
2. Instancia-se `GeracaoQA` (com ou sem cliente LLM).
3. Chama-se o método `run(grafo)`:
   - Extrai triplas do grafo.
   - Para cada tripla (até o limite de `max_pergunta`):
     - Monta prompt few-shot.
     - Gera pergunta e resposta usando o LLM.
     - Loga a geração.
   - Retorna lista de QAs gerados.
4. Os QAs seguem para etapas seguintes (ex: embeddings, avaliação, indexação).
