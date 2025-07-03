# Documentação do Módulo de Persistência Supabase (PersistenciaSupabase.py)

## 1. Propósito

O módulo `PersistenciaSupabase.py` fornece uma interface simplificada para interagir com o banco de dados Supabase. Ele encapsula a lógica de conexão e as operações básicas de manipulação de dados, como criação de tabelas e inserção de registros, tornando o acesso ao Supabase mais fácil e consistente para outras partes do sistema.

## 2. Classe `PersistenciaSupabase`

### `__init__(self)`

O construtor da classe inicializa o cliente Supabase. Ele utiliza as variáveis de ambiente `SUPABASE_URL` e `SUPABASE_KEY` (importadas de `supabase_config.py`) para estabelecer a conexão com o serviço Supabase.

### `criar_tabela(self, sql: str)`

Este método é responsável por executar comandos SQL para criar tabelas no banco de dados Supabase.

*   **`sql` (str)**: A string SQL contendo o comando `CREATE TABLE` a ser executado. É recomendado usar `CREATE TABLE IF NOT EXISTS` para evitar erros caso a tabela já exista.

Exemplo de uso:

```python
# Dentro de outra classe ou função
persistencia = PersistenciaSupabase()
persistencia.criar_tabela("""
    CREATE TABLE IF NOT EXISTS minha_tabela (
        id SERIAL PRIMARY KEY,
        nome TEXT
    );
""")
```

### `inserir(self, tabela: str, dados: dict)`

Este método permite inserir um novo registro em uma tabela específica do Supabase.

*   **`tabela` (str)**: O nome da tabela onde os dados serão inseridos.
*   **`dados` (dict)**: Um dicionário onde as chaves correspondem aos nomes das colunas da tabela e os valores correspondem aos dados a serem inseridos.

Exemplo de uso:

```python
# Dentro de outra classe ou função
persistencia = PersistenciaSupabase()
persistencia.inserir("minha_tabela", {"nome": "Exemplo de Nome"})
```

## 3. Dependências

*   `supabase`: A biblioteca oficial do cliente Python para Supabase.
*   `supabase_config.py`: Módulo que contém as credenciais de conexão (`SUPABASE_URL`, `SUPABASE_KEY`).

## 4. Como Usar

A classe `PersistenciaSupabase` é tipicamente instanciada por módulos que precisam interagir com o banco de dados, como o `PipelineOrquestrador`:

```python
# Exemplo de uso em Orquestrador.py
from persistencia_supabase import PersistenciaSupabase

class PipelineOrquestrador:
    def __init__(self, caminho_pasta):
        self.db = PersistenciaSupabase()
        # ...

    def _criar_tabelas(self):
        self.db.criar_tabela("SQL_DA_TABELA")

    def rodar(self):
        self.db.inserir("nome_da_tabela", {"coluna": "valor"})
```