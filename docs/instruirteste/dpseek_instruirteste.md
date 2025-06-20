Aqui está uma sequência de instruções detalhadas que você pode usar para solicitar que uma IA (como eu) crie testes automatizados para uma classe/função em Python, seguindo os requisitos mencionados:

---

### **Instruções para a IA: Teste de Código Python com Armazenamento em JSON**

1. **Leitura e Análise do Código**  
   - Analise o arquivo Python anexado e identifique todas as funções/métodos públicos que precisam ser testados.  
   - Para cada função, extraia:  
     - Nome da função.  
     - Parâmetros de entrada (com tipos, se disponível).  
     - Comportamento esperado (com base em docstrings ou lógica do código).  

2. **Plano de Testes**  
   - Para cada função, crie um conjunto de casos de teste orientados a resultado, incluindo:  
     - **Cenários válidos** (entradas que devem retornar sucesso).  
     - **Cenários inválidos** (entradas que devem falhar ou levantar exceções).  
     - **Casos extremos** (como valores vazios, nulos, ou formatos incorretos).  
   - Exemplo para uma função `validar_cpf`:  
     ```python
     [
         {"input": "123.456.789-09", "expected": True, "description": "CPF válido com máscara"},
         {"input": "11111111111", "expected": False, "description": "CPF inválido (dígitos repetidos)"},
         {"input": "", "expected": False, "description": "CPF vazio"},
         {"input": None, "expected": False, "description": "CPF None"}
     ]
     ```

3. **Implementação dos Testes**  
   - Use `pytest` ou `unittest` para criar os testes.  
   - Cada teste deve:  
     - Chamar a função com os parâmetros de entrada.  
     - Verificar se o resultado corresponde ao esperado (usar `assert`).  
     - Registrar o resultado em um arquivo JSON estruturado.  

4. **Armazenamento de Evidências em JSON**  
   - Crie um arquivo `test_results.json` com o seguinte formato para cada teste:  
     ```json
     {
         "timestamp": "2024-06-20T12:00:00Z",
         "function_name": "validar_cpf",
         "input": "123.456.789-09",
         "expected": true,
         "actual": true,
         "passed": true,
         "error": null
     }
     ```  
   - Se o teste falhar, capture a exceção ou diferença no campo `error`.

5. **Código de Exemplo para a IA Gerar**  
   - Solicite à IA que gere um script completo, como:  
     ```python
     import json
     import pytest
     from datetime import datetime
     from seu_modulo import validar_cpf  # Substitua pelo módulo real

     def save_test_result(function_name, input_data, expected, actual, error=None):
         result = {
             "timestamp": datetime.utcnow().isoformat(),
             "function_name": function_name,
             "input": str(input_data),
             "expected": expected,
             "actual": actual,
             "passed": expected == actual,
             "error": str(error) if error else None
         }
         with open("test_results.json", "a") as f:
             f.write(json.dumps(result, indent=2) + "\n")

     def test_validar_cpf():
         test_cases = [
             {"input": "123.456.789-09", "expected": True, "description": "CPF válido"},
             {"input": "11111111111", "expected": False, "description": "CPF inválido"}
         ]
         for case in test_cases:
             try:
                 result = validar_cpf(case["input"])
                 assert result == case["expected"]
                 save_test_result("validar_cpf", case["input"], case["expected"], result)
             except Exception as e:
                 save_test_result("validar_cpf", case["input"], case["expected"], None, error=e)
                 pytest.fail(f"Test failed: {e}")
     ```

6. **Integração com n8n (Opcional)**  
   - Se os testes forem ser executados via n8n, adicione uma etapa que:  
     - Execute o script Python (usando o nó `Execute Command`).  
     - Leia o `test_results.json` e envie alertas em caso de falhas (via e-mail, Slack, etc.).  

---

### **Como Usar Estas Instruções**  
1. Envie o arquivo Python à IA com a solicitação:  
   *"Analise este arquivo e gere testes automatizados seguindo o plano acima, com armazenamento em JSON."*  
2. Revise o script gerado e ajuste os casos de teste conforme necessário.  
3. Execute os testes e verifique o arquivo `test_results.json`.

Quer que eu gere um exemplo completo para um arquivo Python específico? Se sim, anexe-o!