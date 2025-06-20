# ANÁLISE DO CÓDIGO

## 1. Mapa de Dependências
Os módulos interagem da seguinte forma:
- `main.py`: Ponto de entrada da aplicação, orquestra o fluxo de execução.
- `Orquestrador.py`: Gerencia a criação de tabelas e a execução do pipeline.
- `PersistenciaSupabase.py`: Responsável pela interação com o banco de dados Supabase.
- `supabase_config.py`: Contém as configurações necessárias para conectar ao Supabase.

## 2. Descrição por Arquivo

### `__init__.py`
- **Propósito**: Este arquivo é intencionalmente deixado em branco, mas serve como um marcador para o pacote.
- **Funções/Classes exportadas**: Nenhuma.
- **Dependências**: Nenhuma.

### `main.py`
- **Propósito**: Ponto de entrada da aplicação, orquestra o fluxo de processamento de dados.
- **Funções/Classes exportadas**: `main()`, `get_supabase_client()`, `salvar_no_supabase()`, e várias funções de etapa.
- **Dependências**: Importa classes de outros módulos e bibliotecas externas como `supabase`.

### `Orquestrador.py`
- **Propósito**: Gerencia a criação de tabelas no Supabase e a execução do pipeline de processamento.
- **Funções/Classes exportadas**: `PipelineOrquestrador`.
- **Dependências**: Importa `PersistenciaSupabase`.

### `PersistenciaSupabase.py`
- **Propósito**: Facilita a interação com o banco de dados Supabase.
- **Funções/Classes exportadas**: `PersistenciaSupabase`.
- **Dependências**: Importa `create_client` do módulo `supabase`.

### `supabase_config.py`
- **Propósito**: Armazena as configurações de conexão com o Supabase.
- **Funções/Classes exportadas**: Nenhuma.
- **Dependências**: Nenhuma.

## 3. Fluxo Executável
1. O fluxo começa em `main.py`, onde a função `main()` é chamada.
2. `main()` cria tabelas no Supabase usando funções específicas.
3. Em seguida, chama várias funções de etapa que processam os dados, desde a ingestão até a avaliação.
4. Os resultados são persistidos no banco de dados Supabase através de `PersistenciaSupabase`.