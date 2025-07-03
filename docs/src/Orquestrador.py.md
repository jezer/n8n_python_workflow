# Documentação do Módulo Orquestrador (Orquestrador.py)

## 1. Propósito

O módulo `Orquestrador.py` define a classe `PipelineOrquestrador`, que é responsável por coordenar e executar o fluxo completo do pipeline de processamento de dados. Ele integra as diversas etapas do pipeline (definidas em `main.py`) e gerencia a persistência dos resultados intermediários e finais no banco de dados Supabase.

## 2. Classe `PipelineOrquestrador`

### `__init__(self, caminho_pasta)`

O construtor da classe inicializa o orquestrador.

*   **`caminho_pasta` (str)**: O caminho para a pasta que contém os arquivos a serem processados pelo pipeline.

Durante a inicialização, ele:
*   Armazena o `caminho_pasta`.
*   Instancia `PersistenciaSupabase` para gerenciar a interação com o banco de dados.
*   Chama o método privado `_criar_tabelas()` para garantir que todas as tabelas necessárias no Supabase existam.
*   Inicializa um dicionário `self.resultados` para armazenar os resultados de cada etapa do pipeline.

### `_criar_tabelas(self)`

Este método privado é responsável por criar todas as tabelas necessárias no banco de dados Supabase, caso elas ainda não existam. Ele itera sobre uma lista de comandos SQL `CREATE TABLE IF NOT EXISTS` para:

*   `triplas_grafo`
*   `metadados_enriquecidos`
*   `qa_gerado`
*   `embeddings`
*   `avaliacoes`

Cada comando SQL é executado através da instância de `PersistenciaSupabase`.

### `rodar(self)`

Este é o método principal que executa o pipeline de ponta a ponta. Ele chama sequencialmente as funções `etapa_X` (que são importadas e definidas em `main.py`) e armazena seus resultados no dicionário `self.resultados`. Além disso, ele gerencia a persistência de dados específicos de cada etapa no Supabase, utilizando os métodos `inserir` da classe `PersistenciaSupabase`.

As etapas executadas incluem (mas não se limitam a):

*   `etapa_ingestao`
*   `etapa_segmentacao`
*   `etapa_limpeza`
*   `etapa_chunking`
*   `etapa_classificacao`
*   `etapa_grafo_conhecimento` (com persistência de triplas)
*   `etapa_geracao_qa` (com persistência de QAs)
*   `etapa_embeddings` (com persistência de embeddings)
*   `etapa_indexacao`
*   `etapa_metadados` (com persistência de metadados)
*   `etapa_hybrid_retriever`
*   `etapa_reranking`
*   `etapa_llm_rag`
*   `etapa_avaliacao` (com persistência de avaliações)
*   `etapa_retriever_adaptativo`
*   `etapa_atualizacao_incremental`
*   `etapa_otimizacao_prompts`
*   `etapa_dashboard`
*   `etapa_alertas`

## 3. Dependências

*   `persistencia_supabase.py`: Para todas as operações de banco de dados com o Supabase.
*   Funções `etapa_X` (ex: `etapa_ingestao`, `etapa_segmentacao`, etc.): Estas funções são definidas no módulo `main.py` e são chamadas pelo `PipelineOrquestrador` para executar as lógicas de cada passo do pipeline.

## 4. Como Usar

A classe `PipelineOrquestrador` é tipicamente instanciada e seu método `rodar()` é chamado a partir do script principal (`main.py`) para iniciar o fluxo de trabalho:

```python
# Exemplo de uso em main.py
from Orquestrador import PipelineOrquestrador

# ... (código para obter caminho_pasta)

pipeline = PipelineOrquestrador(caminho_pasta)
pipeline.rodar()
```