# Documentação do Módulo de Automação Git

## 1. Propósito

Este módulo tem como objetivo automatizar o processo de sincronização, commit e push de alterações para um repositório Git. O script foi simplificado para sempre executar as operações Git quando chamado.

## 2. Componentes

O módulo é composto por um único arquivo principal localizado na pasta `commands`:

-   **`git_auto_commit.ps1`**: Um script PowerShell que executa as operações Git (pull, add, commit, push).

## 3. Como Funciona

O script `git_auto_commit.ps1` segue a seguinte lógica:

1.  `git pull`: Sincroniza o repositório local com as últimas alterações do repositório remoto. Isso evita conflitos e garante que o commit seja feito sobre a versão mais recente.
2.  `git add .`: Adiciona todas as alterações (novos arquivos, modificações, exclusões) na área de staging do Git.
3.  `git commit -m "Automatic sync and commit at [timestamp]"`: Cria um novo commit com uma mensagem padronizada que inclui a data e hora da execução.
4.  `git push`: Envia os commits locais para o repositório remoto.

## 4. Uso

### Executando o Script

Para executar o script `git_auto_commit.ps1`, navegue até o diretório raiz do projeto (`C:\source\IATextHelp\n8n_python_workflow`) e execute o seguinte comando no PowerShell:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\commands\git_auto_commit.ps1
```

## 5. Melhorias Futuras e Considerações

*   **Tratamento de Erros**: Adicionar tratamento de erros mais robusto para as operações Git (ex: falha no pull/push devido a conflitos ou problemas de rede).
*   **Log Detalhado**: Implementar um sistema de log mais detalhado para registrar cada execução, sucesso/falha e as datas envolvidas.
*   **Agendamento**: Para uma automação contínua, o script pode ser agendado para rodar periodicamente usando o Agendador de Tarefas do Windows.
