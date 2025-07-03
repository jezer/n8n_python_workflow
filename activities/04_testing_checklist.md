# Checklist de Testes

Esta lista de verificação deve ser usada para planejar e executar atividades de teste, garantindo a qualidade e a robustez do software.

## Planejamento de Testes

- [ ] **Escopo do Teste:** O que será testado (funcionalidades, módulos, integrações)?
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Tipos de Teste:** Quais tipos de teste serão aplicados (unitário, integração, sistema, aceitação, desempenho, segurança)?
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Ambiente de Teste:** O ambiente de teste está configurado corretamente e isolado do ambiente de produção?
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Dados de Teste:** Dados de teste realistas e representativos foram preparados?
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Critérios de Aceitação:** Os critérios de aceitação para cada funcionalidade estão claros?
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Estratégia de Teste:** A estratégia de teste está definida (ex: top-down, bottom-up, risco-baseado)?
    *   **Evidência de Conclusão:** Relatório de Testes.

## Execução de Testes

- [ ] **Testes Unitários:**
    - [ ] Todos os testes unitários existentes estão passando.
        *   **Evidência de Conclusão:** Relatório de Testes.
    - [ ] Novos testes unitários foram escritos para o código novo/modificado.
        *   **Evidência de Conclusão:** Relatório de Testes.
    - [ ] Os testes unitários cobrem os casos de sucesso e falha.
        *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Testes de Integração:**
    - [ ] Testes de integração foram executados para verificar a comunicação entre módulos.
        *   **Evidência de Conclusão:** Relatório de Testes.
    - [ ] As integrações com serviços externos (ex: Supabase) foram testadas.
        *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Testes de Sistema/Funcionais:**
    - [ ] Todas as funcionalidades foram testadas de acordo com os requisitos.
        *   **Evidência de Conclusão:** Relatório de Testes.
    - [ ] Casos de uso principais e alternativos foram verificados.
        *   **Evidência de Conclusão:** Relatório de Testes.
    - [ ] Fluxos de trabalho completos foram testados.
        *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Testes de Regressão:**
    - [ ] Testes de regressão foram executados para garantir que as novas mudanças não introduziram defeitos em funcionalidades existentes.
        *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Testes de Desempenho (se aplicável):**
    - [ ] O sistema atende aos requisitos de desempenho (tempo de resposta, throughput, uso de recursos).
        *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Testes de Segurança (se aplicável):**
    - [ ] Vulnerabilidades comuns (ex: injeção de SQL, XSS, autenticação) foram verificadas.
        *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] **Testes de Usabilidade (se aplicável):**
    - [ ] A interface do usuário é intuitiva e fácil de usar.
        *   **Evidência de Conclusão:** Relatório de Testes.

## Relatório e Acompanhamento

- [ ] Defeitos encontrados foram registrados com detalhes suficientes (passos para reproduzir, comportamento esperado vs. atual).
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] A severidade e prioridade dos defeitos foram classificadas.
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] O progresso dos testes está sendo acompanhado e comunicado.
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] Os resultados dos testes foram documentados.
    *   **Evidência de Conclusão:** Relatório de Testes.

## Automação de Testes

- [ ] Há oportunidades para automatizar testes manuais?
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] Os testes automatizados são robustos e confiáveis?
    *   **Evidência de Conclusão:** Relatório de Testes.
- [ ] Os testes automatizados são executados como parte do pipeline de CI/CD (se houver)?
    *   **Evidência de Conclusão:** Relatório de Testes.