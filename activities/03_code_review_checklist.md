# Checklist de Revisão de Código

Esta lista de verificação deve ser usada durante a revisão de código para garantir a qualidade, conformidade com as convenções e funcionalidade.

## Conformidade com Convenções (Verificar `docs/rules/coding_conventions.md`)

- [ ] **Formatação:**
    - [ ] Indentação de 4 espaços.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Linhas com no máximo 79 caracteres (código) / 72 caracteres (docstrings/comentários).
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Quebras de linha adequadas para linhas longas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Nomenclatura:**
    - [ ] Módulos e pacotes em `snake_case`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Classes em `PascalCase`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Funções e variáveis em `snake_case`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Constantes em `UPPER_CASE`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Docstrings:**
    - [ ] Presentes para módulos, classes e funções.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Seguem a PEP 257.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Descrevem propósito, `Args:` e `Returns:`.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Type Hinting:**
    - [ ] Anotações de tipo utilizadas para parâmetros e retornos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Importações:**
    - [ ] Agrupadas e ordenadas corretamente (padrão, terceiros, locais).
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Separadas por linhas em branco entre grupos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Tratamento de Erros:**
    - [ ] `try-except` usados para exceções esperadas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
    - [ ] Evitar `except` genéricos.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] **Modularidade:**
    - [ ] Funções e classes pequenas e com responsabilidades únicas.
        *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Funcionalidade e Lógica

- [ ] O código atende aos requisitos da tarefa?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] A lógica é clara e fácil de entender?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] Casos de borda e cenários de erro são tratados adequadamente?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] O código é eficiente (considerando complexidade de tempo/espaço)?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] Há duplicação de código que possa ser refatorada?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Testes

- [ ] Testes unitários/de integração foram adicionados ou atualizados para cobrir as mudanças?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] Os testes existentes ainda passam?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] Os testes cobrem os principais caminhos de execução e casos de borda?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Segurança

- [ ] Não há exposição de credenciais ou informações sensíveis.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] Entradas do usuário são validadas e sanitizadas para prevenir vulnerabilidades (ex: injeção de SQL, XSS).
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Comentários

- [ ] Comentários são claros, concisos e explicam o *porquê*, não apenas o *o quê*.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] Comentários desnecessários ou desatualizados foram removidos.
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.

## Outros

- [ ] O código é legível e bem organizado?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] Há alguma dependência nova que precisa ser adicionada ao `requirements.txt` ou equivalente?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
- [ ] O código está pronto para ser mesclado (merge)?
    *   **Evidência de Conclusão:** Relatório de Revisão de Código.
