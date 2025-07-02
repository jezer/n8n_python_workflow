# Documentação do Módulo de Automação Git

## 1. Propósito

Este módulo tem como objetivo automatizar o processo de sincronização, commit e push de alterações para um repositório Git, com uma condição de execução baseada em uma data limite. Isso garante que as operações Git sejam realizadas apenas dentro de um período pré-definido, permitindo um controle sobre a periodicidade das execuções automáticas.

## 2. Componentes

O módulo é composto por dois arquivos principais localizados na pasta `commands`:

-   **`git_auto_commit.ps1`**: Um script PowerShell que executa as operações Git (pull, add, commit, push) e gerencia a data de controle.
-   **`lastGitCommand.md`**: Um arquivo de texto simples que armazena a data e hora limite para a próxima execução do script `git_auto_commit.ps1`.

## 3. Como Funciona

O script `git_auto_commit.ps1` segue a seguinte lógica:

1.  **Leitura da Data Limite**: O script lê a data e hora contidas no arquivo `lastGitCommand.md`. Esta data representa o limite até o qual o script pode ser executado.
2.  **Verificação Condicional**: Compara a data e hora atual do sistema com a data limite lida do `lastGitCommand.md`.
    *   **Se a data atual for ANTES da data limite**: O script prossegue com as operações Git.
    *   **Se a data atual for DEPOIS ou IGUAL à data limite**: O script não executa as operações Git e exibe uma mensagem informando que a data de execução expirou.
3.  **Operações Git (se a condição for atendida)**:
    *   `git pull`: Sincroniza o repositório local com as últimas alterações do repositório remoto. Isso evita conflitos e garante que o commit seja feito sobre a versão mais recente.
    *   `git add .`: Adiciona todas as alterações (novos arquivos, modificações, exclusões) na área de staging do Git.
    *   `git commit -m "Automatic sync and commit at [timestamp]"`: Cria um novo commit com uma mensagem padronizada que inclui a data e hora da execução.
    *   `git push`: Envia os commits locais para o repositório remoto.
4.  **Atualização da Data Limite (após sucesso)**: Após a conclusão bem-sucedida das operações Git (pull, add, commit, push), o script calcula uma nova data limite adicionando 2 horas à data e hora atual. Esta nova data é então gravada de volta no arquivo `lastGitCommand.md`, definindo o próximo período de execução permitido.

## 4. Uso

### Executando o Script

Para executar o script `git_auto_commit.ps1`, navegue até o diretório raiz do projeto (`C:\source\IATextHelp\n8n_python_workflow`) e execute o seguinte comando no PowerShell:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\commands\git_auto_commit.ps1
```

### Gerenciando `lastGitCommand.md`

O arquivo `lastGitCommand.md` controla quando o script pode ser executado.

*   **Formato da Data**: A data deve estar no formato `yyyy-MM-dd HH:mm:ss` (ex: `2025-07-03 10:00:00`).
*   **Extender Período de Execução**: Para permitir que o script continue executando, você pode editar manualmente `lastGitCommand.md` e definir uma data futura.
*   **Parar Execução Automática**: Para impedir que o script execute, certifique-se de que a data em `lastGitCommand.md` seja uma data passada.

## 5. Melhorias Futuras e Considerações

*   **Configuração de Intervalo**: Atualmente, o intervalo de atualização da data limite é fixo em 2 horas. Uma melhoria seria permitir que este intervalo fosse configurável (ex: via um parâmetro no script ou um arquivo de configuração).
*   **Tratamento de Erros**: Adicionar tratamento de erros mais robusto para as operações Git (ex: falha no pull/push devido a conflitos ou problemas de rede) e para a leitura/escrita do arquivo `lastGitCommand.md`.n*   **Log Detalhado**: Implementar um sistema de log mais detalhado para registrar cada execução, sucesso/falha e as datas envolvidas.
*   **Agendamento**: Para uma automação contínua, o script pode ser agendado para rodar periodicamente usando o Agendador de Tarefas do Windows, em vez de ser executado manualmente.

```