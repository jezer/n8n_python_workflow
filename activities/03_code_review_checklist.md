# Checklist de Revisão de Código

Esta lista de verificação deve ser usada durante a revisão de código para garantir a qualidade, conformidade com as convenções e funcionalidade.

## Conformidade com Convenções (Verificar `docs/rules/coding_conventions.md`)

- [ ] **Formatação:**
    - [ ] Indentação de 4 espaços.
    - [ ] Linhas com no máximo 79 caracteres (código) / 72 caracteres (docstrings/comentários).
    - [ ] Quebras de linha adequadas para linhas longas.
- [ ] **Nomenclatura:**
    - [ ] Módulos e pacotes em `snake_case`.
    - [ ] Classes em `PascalCase`.
    - [ ] Funções e variáveis em `snake_case`.
    - [ ] Constantes em `UPPER_CASE`.
- [ ] **Docstrings:**
    - [ ] Presentes para módulos, classes e funções.
    - [ ] Seguem a PEP 257.
    - [ ] Descrevem propósito, `Args:` e `Returns:`.
- [ ] **Type Hinting:**
    - [ ] Anotações de tipo utilizadas para parâmetros e retornos.
- [ ] **Importações:**
    - [ ] Agrupadas e ordenadas corretamente (padrão, terceiros, locais).
    - [ ] Separadas por linhas em branco entre grupos.
- [ ] **Tratamento de Erros:**
    - [ ] `try-except` usados para exceções esperadas.
    - [ ] Evitar `except` genéricos.
- [ ] **Modularidade:**
    - [ ] Funções e classes pequenas e com responsabilidades únicas.

## Funcionalidade e Lógica

- [ ] O código atende aos requisitos da tarefa?
- [ ] A lógica é clara e fácil de entender?
- [ ] Casos de borda e cenários de erro são tratados adequadamente?
- [ ] O código é eficiente (considerando complexidade de tempo/espaço)?
- [ ] Há duplicação de código que possa ser refatorada?

## Testes

- [ ] Testes unitários/de integração foram adicionados ou atualizados para cobrir as mudanças?
- [ ] Os testes existentes ainda passam?
- [ ] Os testes cobrem os principais caminhos de execução e casos de borda?

## Segurança

- [ ] Não há exposição de credenciais ou informações sensíveis.
- [ ] Entradas do usuário são validadas e sanitizadas para prevenir vulnerabilidades (ex: injeção de SQL, XSS).

## Comentários

- [ ] Comentários são claros, concisos e explicam o *porquê*, não apenas o *o quê*.
- [ ] Comentários desnecessários ou desatualizados foram removidos.

## Outros

- [ ] O código é legível e bem organizado?
- [ ] Há alguma dependência nova que precisa ser adicionada ao `requirements.txt` ou equivalente?
- [ ] O código está pronto para ser mesclado (merge)?