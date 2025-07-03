# Checklist de Revisão de Código

Esta lista de verificação deve ser usada durante a revisão de código para garantir a qualidade, conformidade com as convenções e funcionalidade.

## Conformidade com Convenções (Verificar `docs/rules/coding_conventions.md`)

- [x] **Formatação:**
    - [x] Indentação de 4 espaços.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Linhas com no máximo 79 caracteres (código) / 72 caracteres (docstrings/comentários).
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Quebras de linha adequadas para linhas longas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] **Nomenclatura:**
    - [x] Módulos e pacotes em `snake_case`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Classes em `PascalCase`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Funções e variáveis em `snake_case`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Constantes em `UPPER_CASE`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] **Docstrings:**
    - [x] Presentes para módulos, classes e funções.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Seguem a PEP 257.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Descrevem propósito, `Args:` e `Returns:`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] **Type Hinting:**
    - [x] Anotações de tipo utilizadas para parâmetros e retornos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] **Importações:**
    - [x] Agrupadas e ordenadas corretamente (padrão, terceiros, locais).
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Separadas por linhas em branco entre grupos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] **Tratamento de Erros:**
    - [x] `try-except` usados para exceções esperadas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [x] Evitar `except` genéricos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] **Modularidade:**
    - [x] Funções e classes pequenas e com responsabilidades únicas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Funcionalidade e Lógica

- [x] O código atende aos requisitos da tarefa?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] A lógica é clara e fácil de entender?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] Casos de borda e cenários de erro são tratados adequadamente?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] O código é eficiente (considerando complexidade de tempo/espaço)?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] Há duplicação de código que possa ser refatorada?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Testes

- [x] Testes unitários/de integração foram adicionados ou atualizados para cobrir as mudanças?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] Os testes existentes ainda passam?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] Os testes cobrem os principais caminhos de execução e casos de borda?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Segurança

- [x] Não há exposição de credenciais ou informações sensíveis.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] Entradas do usuário são validadas e sanitizadas para prevenir vulnerabilidades (ex: injeção de SQL, XSS).
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Comentários

- [x] Comentários são claros, concisos e explicam o *porquê*, não apenas o *o quê*.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] Comentários desnecessários ou desatualizados foram removidos.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Outros

- [x] O código é legível e bem organizado?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] Há alguma dependência nova que precisa ser adicionada ao `requirements.txt` ou equivalente?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [x] O código está pronto para ser mesclado (merge)?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).