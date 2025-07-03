# Checklist de Revisão de Código

Esta lista de verificação deve ser usada durante a revisão de código para garantir a qualidade, conformidade com as convenções e funcionalidade.

## Conformidade com Convenções (Verificar `docs/rules/coding_conventions.md`)

- [ ] **Formatação:**
    - [ ] Indentação de 4 espaços.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Linhas com no máximo 79 caracteres (código) / 72 caracteres (docstrings/comentários).
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Quebras de linha adequadas para linhas longas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] **Nomenclatura:**
    - [ ] Módulos e pacotes em `snake_case`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Classes em `PascalCase`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Funções e variáveis em `snake_case`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Constantes em `UPPER_CASE`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] **Docstrings:**
    - [ ] Presentes para módulos, classes e funções.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Seguem a PEP 257.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Descrevem propósito, `Args:` e `Returns:`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] **Type Hinting:**
    - [ ] Anotações de tipo utilizadas para parâmetros e retornos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] **Importações:**
    - [ ] Agrupadas e ordenadas corretamente (padrão, terceiros, locais).
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Separadas por linhas em branco entre grupos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] **Tratamento de Erros:**
    - [ ] `try-except` usados para exceções esperadas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
    - [ ] Evitar `except` genéricos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] **Modularidade:**
    - [ ] Funções e classes pequenas e com responsabilidades únicas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Funcionalidade e Lógica

- [ ] O código atende aos requisitos da tarefa?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] A lógica é clara e fácil de entender?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] Casos de borda e cenários de erro são tratados adequadamente?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] O código é eficiente (considerando complexidade de tempo/espaço)?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] Há duplicação de código que possa ser refatorada?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Testes

- [ ] Testes unitários/de integração foram adicionados ou atualizados para cobrir as mudanças?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] Os testes existentes ainda passam?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] Os testes cobrem os principais caminhos de execução e casos de borda?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Segurança

- [ ] Não há exposição de credenciais ou informações sensíveis.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] Entradas do usuário são validadas e sanitizadas para prevenir vulnerabilidades (ex: injeção de SQL, XSS).
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Comentários

- [ ] Comentários são claros, concisos e explicam o *porquê*, não apenas o *o quê*.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] Comentários desnecessários ou desatualizados foram removidos.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).

## Outros

- [ ] O código é legível e bem organizado?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] Há alguma dependência nova que precisa ser adicionada ao `requirements.txt` ou equivalente?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).
- [ ] O código está pronto para ser mesclado (merge)?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código ([code_review_report.md](code_review_report/2025_07_02_21_00_00/code_review_report.md)).