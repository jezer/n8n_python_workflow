# Checklist de Testes

Esta lista de verificação deve ser usada para planejar e executar atividades de teste, garantindo a qualidade e a robustez do software.

## Planejamento de Testes

- [ ] **Escopo do Teste:** O que será testado (funcionalidades, módulos, integrações)?
- [ ] **Tipos de Teste:** Quais tipos de teste serão aplicados (unitário, integração, sistema, aceitação, desempenho, segurança)?
- [ ] **Ambiente de Teste:** O ambiente de teste está configurado corretamente e isolado do ambiente de produção?
- [ ] **Dados de Teste:** Dados de teste realistas e representativos foram preparados?
- [ ] **Critérios de Aceitação:** Os critérios de aceitação para cada funcionalidade estão claros?
- [ ] **Estratégia de Teste:** A estratégia de teste está definida (ex: top-down, bottom-up, risco-baseado)?

## Execução de Testes

- [ ] **Testes Unitários:**
    - [ ] Todos os testes unitários existentes estão passando.
    - [ ] Novos testes unitários foram escritos para o código novo/modificado.
    - [ ] Os testes unitários cobrem os casos de sucesso e falha.
- [ ] **Testes de Integração:**
    - [ ] Testes de integração foram executados para verificar a comunicação entre módulos.
    - [ ] As integrações com serviços externos (ex: Supabase) foram testadas.
- [ ] **Testes de Sistema/Funcionais:**
    - [ ] Todas as funcionalidades foram testadas de acordo com os requisitos.
    - [ ] Casos de uso principais e alternativos foram verificados.
    - [ ] Fluxos de trabalho completos foram testados.
- [ ] **Testes de Regressão:**
    - [ ] Testes de regressão foram executados para garantir que as novas mudanças não introduziram defeitos em funcionalidades existentes.
- [ ] **Testes de Desempenho (se aplicável):**
    - [ ] O sistema atende aos requisitos de desempenho (tempo de resposta, throughput, uso de recursos).
- [ ] **Testes de Segurança (se aplicável):**
    - [ ] Vulnerabilidades comuns (ex: injeção de SQL, XSS, autenticação) foram verificadas.
- [ ] **Testes de Usabilidade (se aplicável):**
    - [ ] A interface do usuário é intuitiva e fácil de usar.

## Relatório e Acompanhamento

- [ ] Defeitos encontrados foram registrados com detalhes suficientes (passos para reproduzir, comportamento esperado vs. atual).
- [ ] A severidade e prioridade dos defeitos foram classificadas.
- [ ] O progresso dos testes está sendo acompanhado e comunicado.
- [ ] Os resultados dos testes foram documentados.

## Automação de Testes

- [ ] Há oportunidades para automatizar testes manuais?
- [ ] Os testes automatizados são robustos e confiáveis?
- [ ] Os testes automatizados são executados como parte do pipeline de CI/CD (se houver)?