# Documentação do Módulo de Configuração do Supabase (supabase_config.py)

## 1. Propósito

O módulo `supabase_config.py` é responsável por armazenar as configurações essenciais para a conexão com o serviço Supabase. Ele centraliza informações como a URL do projeto, a chave de API e o esquema do banco de dados, facilitando a gestão e o uso dessas credenciais por outros módulos da aplicação.

## 2. Variáveis de Configuração

Este módulo define as seguintes variáveis:

*   **`SUPABASE_URL` (str)**: A URL do seu projeto Supabase. Deve ser substituída pela URL real do seu projeto.
    *   Exemplo: `"https://<SEU-PROJETO>.supabase.co"`
*   **`SUPABASE_KEY` (str)**: A chave de API (anon key ou service role key) do seu projeto Supabase. **ATENÇÃO: Esta chave é sensível e não deve ser comitada diretamente em repositórios públicos.** Recomenda-se fortemente o uso de variáveis de ambiente para gerenciar esta chave em ambientes de produção.
    *   Exemplo: `"<SUA-CHAVE-API>"`
*   **`SUPABASE_SCHEMA` (str)**: O esquema do banco de dados a ser utilizado. O valor padrão é `"public"`.

## 3. Como Usar

Outros módulos que precisam se conectar ao Supabase importam essas variáveis diretamente para configurar o cliente Supabase. Por exemplo:

```python
# Exemplo de uso em PersistenciaSupabase.py
from supabase import create_client
from supabase_config import SUPABASE_URL, SUPABASE_KEY

class PersistenciaSupabase:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
```

## 4. Segurança

É crucial que a `SUPABASE_KEY` não seja exposta em repositórios de código públicos. Para ambientes de produção, siga as melhores práticas de segurança, como:

*   **Variáveis de Ambiente**: Carregue a chave de API de variáveis de ambiente do sistema (ex: `os.environ.get("SUPABASE_KEY")`).
*   **Ferramentas de Gerenciamento de Segredos**: Utilize ferramentas como HashiCorp Vault, AWS Secrets Manager, ou Azure Key Vault.
*   **`.env` files (apenas para desenvolvimento local)**: Use arquivos `.env` (adicionados ao `.gitignore`) para carregar variáveis de ambiente localmente, mas nunca os comite.

**Lembre-se de substituir os valores placeholder (`<SEU-PROJETO>` e `<SUA-CHAVE-API>`) pelos seus valores reais.**