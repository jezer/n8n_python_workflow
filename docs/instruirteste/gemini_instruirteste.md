Com certeza! Como especialista em IA, Python, testes de código e n8n, posso te ajudar a construir uma sequência de instruções eficaz para que uma IA crie testes robustos para o seu código. O foco será em testes orientados a resultados e no armazenamento de evidências.

---

## Instruções para a IA: Criação de Testes de Código Automatizados

Aqui está uma sequência de instruções detalhadas para uma IA gerar testes para suas classes e funções, seguindo os princípios que você descreveu:

---

### 1. Análise e Mapeamento de Funções

* **Instrução para a IA:** "Analise o arquivo Python anexo. Identifique todas as **classes** e **funções** passíveis de teste. Para cada função, extraia sua **assinatura** (nome, parâmetros de entrada e seus tipos esperados, se disponíveis) e, se possível, uma breve descrição de sua **finalidade** ou **comportamento esperado** com base em comentários ou convenções de nomenclatura. Se a função interage com sistemas externos (bancos de dados, APIs), sinalize essa interação."
* **Detalhes e Objetivo:** Esta etapa visa criar um "catálogo" das unidades de código que precisam ser testadas. É crucial para a IA entender o que cada parte do código faz.

---

### 2. Geração de Casos de Teste Orientados a Resultados

* **Instrução para a IA:** "Para cada função identificada, gere um conjunto de **casos de teste diversos e relevantes**. Os testes devem ser **orientados ao resultado**, ou seja, cada caso de teste deve definir:
    * **Entrada de Teste (Input):** Os valores ou condições que serão passados para a função.
    * **Resultado Esperado (Expected Output):** O valor, estado do sistema, ou comportamento que a função deve produzir ao receber a entrada. Considere diferentes cenários:
        * **Casos de Sucesso:** Entradas válidas que devem levar ao comportamento esperado e correto.
        * **Casos de Falha/Erro:** Entradas inválidas, nulas, vazias, ou extremas que devem gerar exceções, `False`, `None`, mensagens de erro específicas, ou outros comportamentos de tratamento de erro.
        * **Casos de Borda (Edge Cases):** Valores mínimos, máximos, limites ou transições que podem expor falhas.
        * **Casos com Efeitos Colaterais (se aplicável):** Se a função modificar o estado de um objeto, banco de dados ou sistema externo, o resultado esperado deve incluir a verificação dessa modificação.
    * **Critérios de Verificação (Assertion Logic):** A lógica que será usada para comparar o resultado real da função com o resultado esperado. Especifique qual método de asserção (ex: `assertEqual`, `assertTrue`, `assertRaises`, `assertIn`, `assertDictEqual`) seria mais adequado para cada verificação."
* **Detalhes e Objetivo:** Esta é a parte central da geração de testes. A IA precisa simular o pensamento de um testador humano, cobrindo uma ampla gama de cenários e definindo claramente o que significa "sucesso" ou "falha" para cada teste.

---

### 3. Construção do Cenário de Teste (Setup e Teardown)

* **Instrução para a IA:** "Para cada função ou grupo de funções que exigem um ambiente específico, defina os passos necessários para **configurar (setup)** o ambiente antes da execução do teste e **limpar (teardown)** o ambiente após a execução. Isso inclui, mas não se limita a:
    * **Mocks/Stubs:** Identifique interações com dependências externas (APIs, bancos de dados) e sugira a criação de mocks ou stubs para isolar a função em teste.
    * **Inicialização de Objetos:** Se a função for um método de classe, especifique como a classe deve ser instanciada e com quais parâmetros.
    * **Preparação de Dados:** Se o teste depender de dados específicos (em banco de dados, arquivos), descreva como esses dados devem ser preparados antes do teste e removidos depois."
* **Detalhes e Objetivo:** Garante que os testes sejam independentes, repetíveis e não deixem resíduos no ambiente de execução.

---

### 4. Geração do Código de Teste

* **Instrução para a IA:** "Com base nos casos de teste e cenários de setup/teardown definidos, gere o **código Python completo** para os testes. Utilize um framework de teste padrão como **`unittest`** ou **`pytest`**. Para cada caso de teste, o código deve:
    * Chamar a função a ser testada com a `Entrada de Teste` definida.
    * Capturar o `Resultado Real` da execução da função.
    * Aplicar os `Critérios de Verificação` (asserções) para comparar o `Resultado Real` com o `Resultado Esperado`.
    * Incluir blocos `try-except` quando for esperado que a função levante exceções, garantindo que a exceção esperada seja capturada e verificada.
    * Gere um arquivo de teste Python (`test_nome_da_classe.py` ou `test_nome_da_funcao.py`) para cada conjunto de testes relevantes."
* **Detalhes e Objetivo:** Transforma as definições abstratas dos testes em código executável.

---

### 5. Registro de Resultados e Evidências em JSON

* **Instrução para a IA:** "Modifique o código de teste gerado para **registrar os detalhes de cada passo do teste e as evidências do resultado em um arquivo JSON**. Para cada execução de caso de teste (bem-sucedida ou falha), o registro JSON deve incluir:
    * `test_name`: Nome descritivo do caso de teste.
    * `function_tested`: Nome da função sendo testada.
    * `input_data`: Os dados de entrada fornecidos à função.
    * `expected_output`: O resultado esperado para este caso de teste.
    * `actual_output`: O resultado real retornado pela função.
    * `status`: "Passed" ou "Failed".
    * `timestamp`: Data e hora da execução do teste.
    * `assertion_message`: A mensagem da asserção, útil em caso de falha.
    * `error_details` (opcional): Rastreamento completo da pilha de erros (`traceback`) se o teste falhar devido a uma exceção não esperada.
    * `evidence` (opcional): Se o teste envolver efeitos colaterais (ex: persistência em DB, chamada a API externa), inclua um campo com a **evidência da verificação do resultado** (ex: estado do banco de dados após a operação, log de chamada da API, snapshot de um arquivo).
    * `setup_details` (opcional): Informações sobre a configuração do ambiente para o teste.
    * `teardown_details` (opcional): Informações sobre a limpeza do ambiente após o teste.
    * Cada execução de teste deve ser um objeto JSON separado em uma lista dentro do arquivo. O arquivo JSON final deve ser nomeado como `test_results_YYYYMMDD_HHMMSS.json`."
* **Detalhes e Objetivo:** Esta é a parte crítica para a "orientação a resultado" e a auditoria. O arquivo JSON se torna um relatório detalhado e uma evidência concreta da execução de cada teste.

---

### Exemplo para a IA (Função de Validação de CPF):

Se a função a ser testada for `validate_cpf(cpf_number)`, as instruções para a IA poderiam resultar em algo como:

**1. Análise:**
* Função: `validate_cpf`
* Assinatura: `validate_cpf(cpf_number: str)`
* Finalidade: "Verifica se um número de CPF é válido de acordo com as regras de validação brasileiras."

**2. Geração de Casos de Teste:**

* **Caso 1 (Inválido):**
    * Entrada: `"111.111.111-11"`
    * Esperado: `False`
    * Verificação: `assertEqual(result, False)`
* **Caso 2 (Válido):**
    * Entrada: `"123.456.789-00"` (substitua por um CPF válido real)
    * Esperado: `True`
    * Verificação: `assertEqual(result, True)`
* **Caso 3 (Vazio):**
    * Entrada: `""`
    * Esperado: `False`
    * Verificação: `assertEqual(result, False)`
* **Caso 4 (Nulo):**
    * Entrada: `None`
    * Esperado: `False`
    * Verificação: `assertEqual(result, False)`
* **Caso 5 (Formato Incorreto):**
    * Entrada: `"12345678900"` (sem pontuação)
    * Esperado: `False`
    * Verificação: `assertEqual(result, False)`

**3. Cenário de Teste:**
* Não há setup/teardown complexo para esta função. É uma função pura.

**4. Geração do Código de Teste (Exemplo usando `unittest`):**

```python
import unittest
import json
import datetime
# Assumindo que a função validate_cpf está em 'your_module.py'
from your_module import validate_cpf 

class TestValidateCpf(unittest.TestCase):

    def setUp(self):
        self.test_results = []

    def tearDown(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=4)

    def run_and_log_test(self, test_name, func, input_data, expected_output, assertion_func, evidence=None):
        test_record = {
            "test_name": test_name,
            "function_tested": func.__name__,
            "input_data": input_data,
            "expected_output": expected_output,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "Failed",
            "assertion_message": ""
        }
        try:
            actual_output = func(input_data)
            assertion_func(actual_output, expected_output)
            test_record["actual_output"] = actual_output
            test_record["status"] = "Passed"
        except AssertionError as e:
            test_record["actual_output"] = actual_output if 'actual_output' in locals() else "Error during execution"
            test_record["assertion_message"] = str(e)
            test_record["status"] = "Failed"
        except Exception as e:
            test_record["actual_output"] = "Exception raised"
            test_record["status"] = "Failed"
            test_record["error_details"] = str(e)
            import traceback
            test_record["traceback"] = traceback.format_exc()
        finally:
            if evidence:
                test_record["evidence"] = evidence
            self.test_results.append(test_record)
            
    def test_invalid_cpf(self):
        self.run_and_log_test(
            "Test CPF Inválido",
            validate_cpf,
            "111.111.111-11",
            False,
            self.assertEqual
        )

    def test_valid_cpf(self):
        self.run_and_log_test(
            "Test CPF Válido",
            validate_cpf,
            "123.456.789-00", # Substitua por um CPF válido real
            True,
            self.assertEqual
        )
        
    def test_empty_cpf(self):
        self.run_and_log_test(
            "Test CPF Vazio",
            validate_cpf,
            "",
            False,
            self.assertEqual
        )

    def test_none_cpf(self):
        self.run_and_log_test(
            "Test CPF Nulo",
            validate_cpf,
            None,
            False,
            self.assertEqual
        )
        
    def test_malformed_cpf(self):
        self.run_and_log_test(
            "Test CPF Malformado",
            validate_cpf,
            "12345678900",
            False,
            self.assertEqual
        )

if __name__ == '__main__':
    unittest.main()
```

---

### Integração com n8n (Considerações Futuras)

Uma vez que a IA gere esses arquivos de teste Python e os relatórios JSON, você pode integrar o processo ao n8n:

1.  **Node "Execute Command":** No n8n, você pode ter um nó que executa o comando `python -m unittest test_your_module.py` ou `pytest test_your_module.py`.
2.  **Node "Read File":** Após a execução, um nó pode ler o arquivo JSON gerado pelos testes.
3.  **Processamento no n8n:** Você pode então usar nós do n8n para:
    * Analisar os resultados do JSON.
    * Enviar notificações (Slack, Email) se testes falharem.
    * Atualizar um banco de dados de status de testes.
    * Disparar fluxos de trabalho adicionais com base nos resultados.

---

Com essas instruções detalhadas, a IA terá um guia claro para gerar testes de alta qualidade, orientados a resultados e com um excelente nível de detalhe para rastreabilidade e depuração.

Há alguma parte dessas instruções que você gostaria de detalhar ainda mais ou que eu possa refinar para seu caso específico?