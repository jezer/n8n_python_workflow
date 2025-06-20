# ANÁLISE DO CÓDIGO

## 1. Mapa de Dependências
Os módulos interagem da seguinte forma:
- `main.py`: Ponto de entrada que orquestra o fluxo do pipeline.
- `Orquestrador.py`: Gerencia a criação de tabelas e a execução do pipeline.
- `PersistenciaSupabase.py`: Responsável pela interação com o banco de dados Supabase.
- `supabase_config.py`: Contém as configurações necessárias para conectar ao Supabase.

## 2. Descrição por Arquivo

### `__init__.py`
- **Propósito principal**: Este arquivo é intencionalmente deixado em branco, mas pode ser usado para expor classes do pipeline.
- **Funções/Classes exportadas**: Nenhuma.
- **Dependências internas/externas**: Nenhuma.

### `main.py`
- **Propósito principal**: Ponto de entrada da aplicação que inicia o pipeline de processamento.
- **Funções/Classes exportadas**: `main()`, `get_supabase_client()`, `salvar_no_supabase()`, e várias funções de etapa.
- **Dependências internas/externas**: Importa módulos de processamento e o cliente Supabase.

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
1. O fluxo começa em `main.py`, onde o caminho da pasta é passado como argumento.
2. O `PipelineOrquestrador` é instanciado e as tabelas são criadas no Supabase.
3. As etapas do pipeline são executadas sequencialmente, desde a ingestão de arquivos até a avaliação contínua.
4. Os dados são persistidos no Supabase em várias tabelas ao longo do processo.