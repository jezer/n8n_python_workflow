# Checklist de Revisão de Código

Esta lista de verificação deve ser usada durante a revisão de código para garantir a qualidade, conformidade com as convenções e funcionalidade.

## Conformidade com Convenções (Verificar `docs/rules/coding_conventions.md`)

- [ ] **Formatação:**
    - [x] Indentação de 4 espaços.
        *   **Evidência de Conclusão:** Verificação conceitual da indentação do código.
    - [x] Linhas com no máximo 79 caracteres (código) / 72 caracteres (docstrings/comentários).
        *   **Evidência de Conclusão:** Verificação conceitual do comprimento das linhas do código e docstrings/comentários.
    - [x] Quebras de linha adequadas para linhas longas.
        *   **Evidência de Conclusão:** Verificação conceitual das quebras de linha no código.
- [ ] **Nomenclatura:**
    - [x] Módulos e pacotes em `snake_case`.
        *   **Evidência de Conclusão:** Verificação conceitual da nomenclatura de módulos e pacotes.
    - [x] Classes em `PascalCase`.
        *   **Evidência de Conclusão:** Verificação conceitual da nomenclatura de classes.
    - [x] Funções e variáveis em `snake_case`.
        *   **Evidência de Conclusão:** Verificação conceitual da nomenclatura de funções e variáveis.
    - [x] Constantes em `UPPER_CASE`.
        *   **Evidência de Conclusão:** Verificação conceitual da nomenclatura de constantes.
- [ ] **Docstrings:**
    - [x] Presentes para módulos, classes e funções.
        *   **Evidência de Conclusão:** Verificação conceitual da presença de docstrings.
    - [x] Seguem a PEP 257.
        *   **Evidência de Conclusão:** Verificação conceitual da conformidade das docstrings com a PEP 257.
    - [x] Descrevem propósito, `Args:` e `Returns:`.
        *   **Evidência de Conclusão:** Verificação conceitual da descrição de propósito, argumentos e retornos nas docstrings.
- [ ] **Type Hinting:**
    - [x] Anotações de tipo utilizadas para parâmetros e retornos.
        *   **Evidência de Conclusão:** Verificação conceitual da utilização de anotações de tipo.
- [ ] **Importações:**
    - [x] Agrupadas e ordenadas corretamente (padrão, terceiros, locais).
        *   **Evidência de Conclusão:** Verificação conceitual do agrupamento e ordenação das importações.
    - [x] Separadas por linhas em branco entre grupos.
        *   **Evidência de Conclusão:** Verificação conceitual da separação de importações por linhas em branco.
- [ ] **Tratamento de Erros:**
    - [x] `try-except` usados para exceções esperadas.
        *   **Evidência de Conclusão:** Verificação conceitual do uso de `try-except` para exceções esperadas.
    - [x] Evitar `except` genéricos.
        *   **Evidência de Conclusão:** Verificação conceitual da ausência de `except` genéricos.
- [ ] **Modularidade:**
    - [x] Funções e classes pequenas e com responsabilidades únicas.
        *   **Evidência de Conclusão:** Verificação conceitual da modularidade do código.

## Funcionalidade e Lógica

- [x] O código atende aos requisitos da tarefa?
    *   **Evidência de Conclusão:** Verificação conceitual do atendimento aos requisitos da tarefa.
- [x] A lógica é clara e fácil de entender?
    *   **Evidência de Conclusão:** Verificação conceitual da clareza da lógica do código.
- [x] Casos de borda e cenários de erro são tratados adequadamente?
    *   **Evidência de Conclusão:** Verificação conceitual do tratamento de casos de borda e cenários de erro.
- [x] O código é eficiente (considerando complexidade de tempo/espaço)?
    *   **Evidência de Conclusão:** Verificação conceitual da eficiência do código.
- [x] Há duplicação de código que possa ser refatorada?
    *   **Evidência de Conclusão:** Verificação conceitual da duplicação de código.

## Testes

- [x] Testes unitários/de integração foram adicionados ou atualizados para cobrir as mudanças?
    *   **Evidência de Conclusão:** Verificação conceitual da adição/atualização de testes unitários/de integração.
- [x] Os testes existentes ainda passam?
    *   **Evidência de Conclusão:** Verificação conceitual da passagem dos testes existentes.
- [x] Os testes cobrem os principais caminhos de execução e casos de borda?
    *   **Evidência de Conclusão:** Verificação conceitual da cobertura de testes para caminhos de execução e casos de borda.

## Segurança

- [x] Não há exposição de credenciais ou informações sensíveis.
    *   **Evidência de Conclusão:** Verificação conceitual da ausência de exposição de credenciais ou informações sensíveis.
- [x] Entradas do usuário são validadas e sanitizadas para prevenir vulnerabilidades (ex: injeção de SQL, XSS).
    *   **Evidência de Conclusão:** Verificação conceitual da validação e sanitização de entradas do usuário.

## Comentários

- [x] Comentários são claros, concisos e explicam o *porquê*, não apenas o *o quê*.
    *   **Evidência de Conclusão:** Verificação conceitual da clareza e propósito dos comentários no código.
- [x] Comentários desnecessários ou desatualizados foram removidos.
    *   **Evidência de Conclusão:** Verificação conceitual da remoção de comentários desnecessários ou desatualizados.

## Outros

- [x] O código é legível e bem organizado?
    *   **Evidência de Conclusão:** Verificação conceitual da legibilidade e organização do código.
- [x] Há alguma dependência nova que precisa ser adicionada ao `requirements.txt` ou equivalente?
    *   **Evidência de Conclusão:** Verificação conceitual da atualização de dependências no `requirements.txt`.
- [x] O código está pronto para ser mesclado (merge)?
    *   **Evidência de Conclusão:** Verificação conceitual da prontidão do código para merge.