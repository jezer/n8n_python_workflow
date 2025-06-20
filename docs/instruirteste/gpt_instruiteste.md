Beleza! Aqui vai um roteiro de prompts pra IA gerar tests de uma classe em Python pra uso no n8n:

1. **Carregar e analisar o arquivo**

   * “Leia o arquivo `<nome_do_arquivo>.py` e identifique todas as classes e funções públicas que precisam de teste.”
   * *Fonte: pytest docs*

2. **Mapear cenários de teste**

   * “Para cada função, liste casos positivos, negativos e limites (ex: inputs válidos, inválidos e vazios).”
   * *Fonte: pytest docs*

3. **Gerar código de teste**

   * “Construa um suite de testes em `tests/test_<nome>.py` usando pytest/unittest, com funções nomeadas seguindo `test_<funcao>_<cenario>()`.”
   * *Fonte: Python unittest*

4. **Assert orientado a resultado**

   * “Em cada teste, chame a função e use asserts para confirmar que o retorno ou efeito colateral bate com o esperado.”
   * *Fonte: pytest docs*

5. **Registrar evidências em JSON**

   * “Após cada assert, capture num dicionário: nome do teste, input, output obtido e status (pass/fail). Ao fim da suíte, salve tudo em `reports/report.json`.”
   * *Fonte: pytest docs*

6. **Integrar no n8n**

   * “Gere um workflow n8n que execute `pytest --json-report --json-report-file=reports/report.json` e retorne o JSON como output de um node HTTP Request.”
   * *Fonte: n8n docs*

7. **Validar JSON de saída**

   * “No n8n, adicione um node Function que leia `report.json`, valide a estrutura (ex: cada item tem “test\_name”, “status”, “details”) e lance erro se algo falhar.”
   * *Fonte: n8n docs*

Use esses prompts pra IA orquestrar todo o processo de teste automatizado. Qualquer dúvida, só dar um toque!
