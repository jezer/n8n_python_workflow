### Proposta de Convenções de Código e Documentação

#### 1. Convenções de Código (Python)

Para o código Python, a base será a **PEP 8**, que é o guia de estilo oficial para Python.

*   **Formatação:**
    *   **Indentação:** 4 espaços para cada nível de indentação.
    *   **Comprimento da Linha:** Máximo de 79 caracteres (para código) e 72 caracteres (para docstrings e comentários).
    *   **Quebras de Linha:** Use parênteses, colchetes ou chaves para quebrar linhas longas.
*   **Nomenclatura:**
    *   **Módulos e Pacotes:** `snake_case` (ex: `meu_modulo.py`, `meu_pacote/`).
    *   **Classes:** `PascalCase` (ex: `MinhaClasse`).
    *   **Funções e Variáveis:** `snake_case` (ex: `minha_funcao()`, `minha_variavel`).
    *   **Constantes:** `UPPER_CASE` (ex: `MINHA_CONSTANTE`).
*   **Docstrings:**
    *   Utilize docstrings para módulos, classes e funções, seguindo a **PEP 257**.
    *   Use aspas triplas (`"""Docstring aqui."""`).
    *   Descreva o propósito, parâmetros (`Args:`), e o que a função retorna (`Returns:`).
*   **Type Hinting:**
    *   Sempre que possível, utilize anotações de tipo (type hints) para parâmetros de funções e valores de retorno. Isso melhora a legibilidade e a capacidade de detecção de erros por ferramentas.
*   **Importações:**
    *   Agrupe as importações na seguinte ordem:
        1.  Módulos da biblioteca padrão.
        2.  Módulos de terceiros.
        3.  Módulos locais do projeto.
    *   Cada grupo deve ser separado por uma linha em branco.
    *   As importações dentro de cada grupo devem ser ordenadas alfabeticamente.
*   **Tratamento de Erros:**
    *   Utilize blocos `try-except` para lidar com exceções esperadas.
    *   Evite `except` genéricos sem especificar o tipo de exceção.
*   **Modularidade:**
    *   Mantenha funções e classes pequenas e com responsabilidades únicas.

#### 2. Convenções de Documentação

Esta seção incorpora sua sugestão para a estrutura da pasta `docs`.

*   **Localização:** Toda a documentação relacionada a um arquivo de código específico deve residir na pasta `docs`.
*   **Estrutura de Pastas em `docs`:
    *   Para **qualquer arquivo** que necessite de documentação detalhada (seja um arquivo Python em `src/`, um script em `commands/`, etc.), crie uma estrutura de pastas dentro de `docs/` que espelhe o caminho relativo do arquivo original.
    *   A documentação para um arquivo específico deve ser um arquivo Markdown (`.md`) com o **mesmo nome base** do arquivo original.
    *   **Exemplos:
        *   Para `src/1.Ingestao/A.ingestao_de_arquivos/main_ingestao.py`, a documentação estará em `docs/src/1.Ingestao/A.ingestao_de_arquivos/main_ingestao.md`.
        *   Para `commands/git_auto_commit.ps1`, a documentação estará em `docs/commands/git_auto_commit.md`.
    *   **Evitar Repetição de Nomes:** Garanta que os nomes dos arquivos de código sejam únicos em todo o projeto para que a estrutura de documentação funcione sem ambiguidades.
*   **Nomenclatura de Arquivos de Documentação:**
    *   O arquivo de documentação principal para uma unidade de código (ex: `docs/commands/git_auto_commit.md`) deve ter o **mesmo nome base** do arquivo de código que ele documenta.
    *   Para arquivos de documentação **suplementares** dentro de uma pasta de documentação (ex: `docs/src/meu_modulo/`), use nomes descritivos, em minúsculas e separados por hífens (ex: `visao_geral.md`, `uso.md`, `referencia_api.md`, `fluxo_dados.mmd`).
*   **Formato:**
    *   **Texto:** Markdown (`.md`).
    *   **Diagramas:** Mermaid (`.mmd`).
*   **Idioma:** Português do Brasil (pt-BR), conforme já estabelecido.
*   **Conteúdo Mínimo por Módulo/Arquivo de Código:**
    *   `visao_geral.md`: Uma descrição de alto nível do propósito do módulo/arquivo.
    *   `uso.md`: Exemplos de como usar as funções ou classes principais.
    *   `referencia_api.md` (opcional, se a docstring não for suficiente): Detalhes sobre funções, classes, parâmetros e valores de retorno.
    *   `fluxo_dados.mmd` (opcional): Diagramas de fluxo ou sequência usando Mermaid para explicar a lógica interna.

#### 3. Convenções Gerais do Projeto

*   **Mensagens de Commit:**
    *   Claras, concisas e descritivas, em português.
    *   Sugiro usar um estilo como o Conventional Commits (ex: `feat:`, `fix:`, `docs:`, `refactor:`), seguido de uma breve descrição.
    *   Exemplo: `feat: Adiciona nova funcionalidade de ingestão de dados`
*   **Revisão de Código:**
    *   Incentivar a revisão de código por pares para garantir a adesão às convenções e a qualidade do código.
