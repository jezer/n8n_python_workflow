# Checklist de Revisão de Código

Esta lista de verificação deve ser usada durante a revisão de código para garantir a qualidade, conformidade com as convenções e funcionalidade.

## Conformidade com Convenções (Verificar `docs/rules/coding_conventions.md`)

- [ ] **Formatação:**
    - [x] Indentação de 4 espaços. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Linhas com no máximo 79 caracteres (código) / 72 caracteres (docstrings/comentários). (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Quebras de linha adequadas para linhas longas. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Nomenclatura:**
    - [x] Módulos e pacotes em `snake_case`. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Classes em `PascalCase`. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Funções e variáveis em `snake_case`. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Constantes em `UPPER_CASE`. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Docstrings:**
    - [x] Presentes para módulos, classes e funções. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Seguem a PEP 257. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Descrevem propósito, `Args:` e `Returns:`. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Type Hinting:**
    - [x] Anotações de tipo utilizadas para parâmetros e retornos. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Importações:**
    - [x] Agrupadas e ordenadas corretamente (padrão, terceiros, locais). (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Separadas por linhas em branco entre grupos. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Tratamento de Erros:**
    - [x] `try-except` usados para exceções esperadas. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [x] Evitar `except` genéricos. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Modularidade:**
    - [x] Funções e classes pequenas e com responsabilidades únicas. (Concluído em 2025-07-02 23:46:00)
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Funcionalidade e Lógica

- [x] O código atende aos requisitos da tarefa? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] A lógica é clara e fácil de entender? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] Casos de borda e cenários de erro são tratados adequadamente? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] O código é eficiente (considerando complexidade de tempo/espaço)? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] Há duplicação de código que possa ser refatorada? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Testes

- [x] Testes unitários/de integração foram adicionados ou atualizados para cobrir as mudanças? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] Os testes existentes ainda passam? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] Os testes cobrem os principais caminhos de execução e casos de borda? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Segurança

- [x] Não há exposição de credenciais ou informações sensíveis. (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] Entradas do usuário são validadas e sanitizadas para prevenir vulnerabilidades (ex: injeção de SQL, XSS). (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Comentários

- [x] Comentários são claros, concisos e explicam o *porquê*, não apenas o *o quê*. (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] Comentários desnecessários ou desatualizados foram removidos. (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Outros

- [x] O código é legível e bem organizado? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] Há alguma dependência nova que precisa ser adicionada ao `requirements.txt` ou equivalente? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [x] O código está pronto para ser mesclado (merge)? (Concluído em 2025-07-02 23:46:00)
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
