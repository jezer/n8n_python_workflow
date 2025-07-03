# Regras de Gestão de Atividades

Para garantir a clareza, rastreabilidade e padronização na execução das atividades do projeto, as seguintes regras devem ser seguidas:

## 1. Estrutura dos Checklists de Atividades

Todos os arquivos de checklist na pasta `activities/` devem seguir estas diretrizes:

1.1.  **Numeração Sequencial:** Cada item de atividade e sub-item deve ser numerado sequencialmente (ex: `1.`, `1.1`, `1.2`, `2.`, `2.1`).
1.2.  **Evidência de Conclusão:** Para cada atividade, deve ser claramente definido qual será a "evidência de conclusão". Esta evidência pode ser um arquivo, um screenshot, um log, um hash de commit, um link para um sistema externo, etc. A descrição da evidência deve ser concisa e clara.

## 2. Armazenamento de Evidências de Conclusão

Ao concluir uma atividade, a evidência correspondente deve ser armazenada em uma estrutura de pastas padronizada dentro da pasta `activities/`.

2.1.  **Estrutura do Caminho:** A evidência deve ser salva no seguinte formato de caminho:
    `activities/<nome_do_arquivo_checklist_base>/<nome_da_atividade_curto>/yyyy_mm_dd_hh_MM_ss/*.*`

    *   `<nome_do_arquivo_checklist_base>`: O nome base do arquivo de checklist (ex: `01_general_project_tasks`).
    *   `<nome_da_atividade_curto>`: Um nome curto e descritivo (em `snake_case`) da atividade específica que está sendo evidenciada (ex: `escopo_definido`, `marcos_prazos`).
    *   `yyyy_mm_dd_hh_MM_ss`: Um timestamp da data e hora da conclusão da atividade, garantindo unicidade e ordenação cronológica.
    *   `*.*`: O(s) arquivo(s) de evidência.

2.2.  **Exemplo:**
    Se a atividade "Escopo do projeto definido e comunicado" do checklist `01_general_project_tasks.md` for concluída em 2 de julho de 2025 às 14:30:00, e a evidência for um arquivo `escopo.pdf`, o caminho seria:
    `activities/01_general_project_tasks/escopo_definido/2025_07_02_14_30_00/escopo.pdf`

## 3. Atualização do Checklist

Após a conclusão de uma atividade e o armazenamento da evidência:

3.1.  O item correspondente no arquivo de checklist (`activities/<nome_do_arquivo_checklist_base>.md`) deve ser marcado como concluído (ex: de `- [ ]` para `- [x]`).
3.2.  Uma referência à evidência deve ser adicionada ao lado do item concluído no checklist, preferencialmente como um link relativo para a pasta da evidência.
