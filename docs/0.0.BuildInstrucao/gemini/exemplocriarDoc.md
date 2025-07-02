# Documentação do Arquivo `create.py`

*Documentação gerada estritamente com base no conteúdo do arquivo fornecido, sem extrapolações ou informações externas.*

## Visão Geral
O arquivo `create.py` é um módulo Python que implementa funcionalidades para:
- Execução de notebooks Databricks em paralelo
- Gerenciamento de estratégias de execução
- Criação e manipulação de tabelas e views no Databricks Unity Catalog
- Controle de versões e histórico de tabelas
- Operações de ETL com suporte a cargas incrementais

## Estrutura Principal

### 1. Classes Principais

#### `Monit_StartEnd_Time`
Classe utilitária para monitoramento de tempo de execução:
```python
class Monit_StartEnd_Time:
    def Start(self, FunctionName):
        # Registra início da execução
        self._start_time = datetime.now()
    
    def End(self):
        # Calcula e exibe tempo total de execução
        self._total_time = self._end_time - self._start_time
```

#### `Notebook`
Dataclass para representar notebooks a serem executados:
```python
@dataclass
class Notebook:
    path: str          # Caminho do notebook
    timeout: int = 0   # Tempo limite de execução
    parameters: dict = None  # Parâmetros de execução
    retry: int = 0     # Número de tentativas
    enabled: bool = True  # Se está habilitado
```

#### `CreateObj`
Classe principal que herda de `SparkHelper` e implementa as operações de criação e gerenciamento:
```python
class CreateObj(SparkHelper):
    def __init__(self, objparameters=None, DebugMode=False, LogOnTable=False, _tags=None):
        # Inicialização com parâmetros de configuração
        self._listTables = []
        self._var_parameters = [
            "com_truncate", "insert_if_exists", "onlycreate", "force_insert", 
            "DropTableAndCreate", "CreateVersionTable", "tabela_encontrada", "dt_ini"
        ]
```

### 2. Principais Funcionalidades

#### Execução de Notebooks
- `ExecuteContainers`: Executa múltiplos notebooks baseado em um dataframe de entrada
- `executeNotebook`: Executa um notebook individual com tratamento de erros
- `executeNotebooks`: Execução paralela de notebooks usando ThreadPoolExecutor
- `ExecutarTodosNotebooks`: Orquestra a execução completa de uma estratégia

```python
def executeNotebooks(notebooks:List[Notebook], maxParallel:int, _SpkHelp:object):
    with ThreadPoolExecutor(max_workers=maxParallel) as executor:
        results = [executor.submit(executeNotebook, notebook, _SpkHelp) 
                  for notebook in notebooks if notebook.enabled]
        return [tryFuture(r) for r in results]
```

#### Gerenciamento de Workspace
- `GetAllWorkspace`: Lista todos os notebooks e diretórios em um workspace
- `LerTodosWorkspace`: Inicia o processo de mapeamento do workspace

```python
def GetAllWorkspace(PathComplement, FieldsDetails, _SpkHelp):
    # Utiliza a API do Databricks para listar conteúdo do workspace
    url = f'{instance}/api/2.0/workspace/list'
    response = requests.get(url, headers=headers, data=data_path)
```

#### Operações com Tabelas
- `OperacoesTabelas`: Método principal para criação/atualização de tabelas
- `createDeliveryView`: Cria views no schema delivery
- `createSharedView`: Cria views compartilhadas entre containers
- `manage_table_versioning`: Gerencia versionamento de tabelas

```python
def OperacoesTabelas(self, db_cat_table, select_text, ds_comentario, source_tables, Funcoes):
    # Implementa lógica complexa para criação/atualização de tabelas com múltiplas opções:
    # - Criação nova
    # - Truncate e recarga
    # - Insert if exists
    # - Versionamento
```

#### Controle Incremental
- `CapturarFullCongelada_e_Incremental`: Gerencia cargas incrementais com histórico
- `verificar_e_atualizar_historico`: Atualiza tabelas históricas a partir de fontes congeladas

```python
def CapturarFullCongelada_e_Incremental(
    self, table_destino, table_root, campoParticao, key_delete, ds_comentario,
    periodoIni=None, periodoFim=None, full_congelado_table=None, Select_columns=None):
    # Implementa lógica completa para cargas incrementais com:
    # - Verificação de existência de históricos
    # - Carga inicial a partir de fontes congeladas
    # - Atualização incremental
```

### 3. Utilitários Importantes

#### Controle de Tempo
```python
def GetLastUpdateTable(db_cat_tabela, _SpkHelp):
    # Obtém a última atualização de uma tabela consultando seu histórico
    history_df = _SpkHelp.Get_TableHistory(db_cat_tabela)
```

#### Conversão de Dados
```python
def converter_para_datetime(self, dt_referencia):
    # Converte diversos formatos de data para datetime
    # Suporta: strings numéricas, timestamps epoch, objetos date
```

#### Gerenciamento de Versões
```python
def rename_table(self, full_table_name, timestamp):
    # Cria versão backup de tabela com timestamp
    queryCreate = f"CREATE TABLE IF NOT EXISTS {full_backup_table_name} LIKE {full_table_name}"
```

## Fluxos Principais

1. **Execução de Estratégias**:
   - `ExecutarEstrategia` → `LerTodosWorkspace` → `ExecutarTodosNotebooks`
   - Envolve mapeamento do workspace e execução ordenada de notebooks

2. **Criação de Tabelas/Views**:
   - `CreateObj` oferece diversos métodos para criação de objetos:
     - `createDeliveryView`/`createSharedView` para views
     - `OperacoesTabelas` para tabelas com múltiplas opções

3. **Cargas Incrementais**:
   - `CapturarFullCongelada_e_Incremental` gerencia todo o ciclo:
     - Verifica existência de históricos
     - Cria estrutura inicial se necessário
     - Atualiza a partir de fontes congeladas
     - Processa incrementos

## Observações
- O código faz uso extensivo de um objeto `_SpkHelp` (provavelmente uma instância de `SparkHelper`) que fornece métodos utilitários para operações no Databricks
- Várias operações são registradas em tabelas de controle no schema `prd_controle`
- O sistema implementa um mecanismo completo de semáforo para controle de execução

*Documentação gerada estritamente com base no conteúdo do arquivo fornecido, conforme solicitado nos parâmetros de configuração.*