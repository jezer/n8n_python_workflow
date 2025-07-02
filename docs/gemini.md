# Contexto do Projeto: IATextHelp/n8n_python_workflow

## 1. Sobre o Projeto

Este repositório contém a documentação, protótipos e instruções para um sistema de automação que integra n8n, Python e bancos de dados (PostgreSQL/Supabase). O objetivo principal é explorar o uso de LLMs (como o Gemini) para auxiliar no desenvolvimento, documentação e teste de software.

O projeto está organizado em torno de "instruções" para diferentes modelos de IA, diagramas de fluxo e arquitetura, e protótipos de interfaces.

## 2. Tecnologias Principais

- **Linguagem Principal:** Python
- **Automação de Workflow:** n8n
- **Banco de Dados:** PostgreSQL (via Supabase)
- **Diagramas:** Mermaid (`.mmd`) para fluxogramas, diagramas de sequência, mind maps, etc.
- **Idioma:** A grande maioria dos documentos e nomes de arquivos está em português do Brasil (pt-BR).

## 3. Convenções e Regras do Projeto

Para detalhes sobre as convenções e regras do projeto, consulte os arquivos na pasta `docs/rules/`:

- [Regras de Operações Git](rules/git_operations.md)
- [Regras de Idioma e Estilo Geral](rules/language_and_style.md)
- [Convenções de Código (Python)](rules/coding_conventions.md)
- [Convenções de Documentação](rules/documentation_conventions.md)
- [Exceções de Pastas](rules/folder_exceptions.md)


## 4. Instruções Específicas para o Gemini

- Ao gerar código Python, siga as convenções encontradas nos arquivos da pasta `help/`.
- Ao gerar documentação, siga o estilo dos arquivos `.md` existentes.
- Ao ser solicitado para criar um fluxo ou diagrama, gere o código em formato Mermaid (`.mmd`).
- Após cada alteração bem-sucedida (criação, modificação ou exclusão de arquivos), adicione os arquivos ao stage do Git, crie um commit com uma mensagem descritiva e execute o push para o repositório remoto.
- Sempre guarde todas as execuções no arquivo de log_yyyy_mm_dd_hh_MM_ss.txt