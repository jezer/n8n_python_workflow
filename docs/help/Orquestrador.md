# ANÁLISE DO CÓDIGO

## 1. Mapa de Dependências
Os módulos interagem da seguinte forma:
- `main.py`: Ponto de entrada da aplicação, orquestra o fluxo de execução.
- `Orquestrador.py`: Gerencia a criação de tabelas e a execução do pipeline.
- `PersistenciaSupabase.py`: Responsável pela interação com o banco de dados Supabase.
- `supabase_config.py`: Contém as configurações necessárias para conectar ao Supabase.

## 2. Descrição por Arquivo

### `__init__.py`
- **Propósito principal**: Este arquivo é intencionalmente deixado em branco, mas pode ser usado para expor classes principais do pipeline.
- **Funções/Classes exportadas**: Nenhuma.
- **Dependências internas/externas**: Nenhuma.

### `main.py`
- **Propósito principal**: Ponto de entrada da aplicação que inicia o pipeline de processamento.
- **Funções/Classes exportadas**: `main()`, `get_supabase_client()`, `salvar_no_supabase()`, e várias funções de etapa.
- **Dependências internas/externas**: Importa módulos de processamento e configuração do Supabase.

### `Orquestrador.py`
- **Propósito principal**: Orquestra a execução do pipeline e a criação de tabelas no Supabase.
- **Funções/Classes exportadas**: `PipelineOrquestrador`.
- **Dependências internas/externas**: Importa `PersistenciaSupabase`.

### `PersistenciaSupabase.py`
- **Propósito principal**: Gerencia a persistência de dados no Supabase.
- **Funções/Classes exportadas**: `PersistenciaSupabase`.
- **Dependências internas/externas**: Importa `create_client` do módulo `supabase`.

### `supabase_config.py`
- **Propósito principal**: Armazena as configurações de conexão com o Supabase.
- **Funções/Classes exportadas**: Nenhuma.
- **Dependências internas/externas**: Nenhuma.

## 3. Fluxo Executável
1. O fluxo começa em `main.py`, onde a função `main()` é chamada.
2. `main()` cria as tabelas necessárias no Supabase.
3. Em seguida, chama as funções de etapa que processam os dados:
   - `etapa_ingestao()`
   - `etapa_segmentacao()`
   - `etapa_limpeza()`
   - `etapa_chunking()`
   - `etapa_classificacao()`
   - `etapa_grafo_conhecimento()`
   - `etapa_geracao_qa()`
   - `etapa_embeddings()`
   - `etapa_indexacao()`
   - `etapa_metadados()`
   - `etapa_hybrid_retriever()`
   - `etapa_reranking()`
   - `etapa_llm_rag()`
   - `etapa_avaliacao()`
   - `etapa_retriever_adaptativo()`
   - `etapa_atualizacao_incremental()`
   - `etapa_otimizacao_prompts()`
   - `etapa_dashboard()`
   - `etapa_alertas()`
4. Cada etapa é responsável por uma parte do processamento e pode interagir com o banco de dados Supabase através de `PersistenciaSupabase.py`.