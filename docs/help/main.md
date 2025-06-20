# ANÁLISE DO CÓDIGO

## 1. Mapa de Dependências
Os módulos interagem da seguinte forma:
- `main.py` é o ponto de entrada da aplicação e orquestra o fluxo de execução.
- `Orquestrador.py` gerencia a criação de tabelas e a execução do pipeline.
- `PersistenciaSupabase.py` é responsável pela interação com o banco de dados Supabase.
- `supabase_config.py` contém as configurações necessárias para conectar ao Supabase.

## 2. Descrição por Arquivo

### `__init__.py`
- **Propósito principal**: Este arquivo é intencionalmente deixado em branco, mas serve para indicar que o diretório é um pacote Python.
- **Funções/Classes exportadas**: Nenhuma.
- **Dependências internas/externas**: Nenhuma.

### `main.py`
- **Propósito principal**: Ponto de entrada da aplicação, orquestra o fluxo de processamento de dados.
- **Funções/Classes exportadas**: `main()`, `get_supabase_client()`, `salvar_no_supabase()`, e várias funções de etapa.
- **Dependências internas/externas**: Importa módulos de processamento, Supabase e o orquestrador.

### `Orquestrador.py`
- **Propósito principal**: Gerencia a criação de tabelas no Supabase e a execução do pipeline de processamento.
- **Funções/Classes exportadas**: `PipelineOrquestrador`.
- **Dependências internas/externas**: Importa `PersistenciaSupabase`.

### `PersistenciaSupabase.py`
- **Propósito principal**: Facilita a interação com o banco de dados Supabase.
- **Funções/Classes exportadas**: `PersistenciaSupabase`.
- **Dependências internas/externas**: Importa `create_client` do módulo `supabase`.

### `supabase_config.py`
- **Propósito principal**: Armazena as configurações de conexão com o Supabase.
- **Funções/Classes exportadas**: Nenhuma.
- **Dependências internas/externas**: Nenhuma.

## 3. Fluxo Executável
1. O fluxo começa em `main.py`, onde a função `main()` é chamada.
2. O caminho da pasta é passado para `PipelineOrquestrador`, que inicia o processo.
3. O `Orquestrador.py` cria as tabelas necessárias no Supabase.
4. As etapas de processamento são executadas sequencialmente, desde a ingestão até a avaliação.
5. Os resultados são persistidos no Supabase através de `PersistenciaSupabase.py`.