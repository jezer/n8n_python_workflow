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

## 3. Convenções do Projeto

- **Idioma:** Sempre que criar ou modificar arquivos, utilize **português do Brasil**, a menos que seja instruído do contrário. Isso se aplica a comentários no código, documentação e mensagens de commit.
- **Diagramas:** Ao criar ou editar diagramas, utilize la sintaxe **Mermaid**. Salve novos diagramas com a extensão `.mmd`.
- **Estrutura de Pastas:**
    - `0.0.BuildInstrucao`: Contém os critérios e exemplos para construir instruções para as IAs.
    - `1.Ingestao`, `1.1classificao`: Etapas do fluxo principal de processamento de dados.
    - `comentarios`: Armazena diversos tipos de diagramas que documentam o sistema.
    - `help`: Documentação de módulos Python específicos como `Orquestrador` e `PersistenciaSupabase`.
    - `instruirteste`: Instruções para a criação de testes.
    - `n8n_postgree`: Detalhes da integração entre n8n e o banco de dados.
- **Instruções para IAs:** Note que existem arquivos específicos para diferentes modelos (`gemini_...`, `dpseek_...`, `gpt_...`). Ao gerar novas instruções, siga este padrão.

## 4. Instruções para o Gemini

- Ao gerar código Python, siga as convenções encontradas nos arquivos da pasta `help/`.
- Ao gerar documentação, siga o estilo dos arquivos `.md` existentes.
- Ao ser solicitado para criar um fluxo ou diagrama, gere o código em formato Mermaid (`.mmd`).
- Após cada alteração bem-sucedida (criação, modificação ou exclusão de arquivos), adicione os arquivos ao stage do Git, crie um commit com uma mensagem descritiva e execute o push para o repositório remoto.
