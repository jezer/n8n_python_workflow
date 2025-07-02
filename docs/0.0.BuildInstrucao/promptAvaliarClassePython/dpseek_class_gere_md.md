**Prompt para Análise Detalhada de Arquivo Python com Geração de Documentação em Markdown**  

---  

### **Instruções para a IA:**  
**Objetivo Principal:**  
Analisar **exclusivamente** o conteúdo do arquivo Python (.py) fornecido e gerar um documento técnico em Markdown (.md) com uma explicação detalhada, precisa e **100% baseada no código fonte**, sem adições criativas ou suposições externas.  

---  

### **Configurações Obrigatórias:**  
| Parâmetro        | Valor       | Efeito Garantido |  
|------------------|-------------|------------------|  
| **Modelo**       | (Melhor compreensão contextual disponível) | Prioriza análise técnica precisa. |  
| **Temperatura**  | **0.1**     | Respostas determinísticas, zero invenções. |  
| **Top P**        | **0.3**     | Foca apenas nos tokens mais relevantes do código. |  
| **Freq. Penalty**| **1.0**     | Elimina repetições desnecessárias de termos. |  
| **Pres. Penalty**| **1.5**     | Bloqueia qualquer informação não presente no arquivo. |  

---  

### **Requisitos do Documento Markdown:**  
1. **Estrutura do Arquivo:**  
   ```markdown
   # Análise Técnica: `[NOME_DO_ARQUIVO].py`  

   ## 1. **Metadados**  
      - **Autor:** [Extrair de comentários, se houver]  
      - **Data:** [Extrair de comentários ou versão]  
      - **Licença:** [Se mencionada]  

   ## 2. **Propósito Principal**  
      - [Descrição objetiva baseada em comentários ou função principal. Ex.: "Implementa um algoritmo de ordenação QuickSort."]  

   ## 3. **Estrutura do Código (Linha por Linha)**  
      ### **Imports**  
      ```python
      [Listar todos os imports]  
      ```  
      **Finalidade de Cada Biblioteca:** [Ex.: "`pandas`: Manipulação de dados em DataFrame."]  

      ### **Classes/Funções**  
      ```python
      [Trecho do código da classe/função principal]  
      ```  
      - **Parâmetros:** [Nome | Tipo (se tipado) | Descrição (extraída de docstrings/comentários)]  
      - **Lógica:** [Explicação passo a passo do fluxo, **apenas com base no código**]  

   ## 4. **Variáveis Globais/Constantes**  
      | Nome          | Valor/Tipo  | Contexto de Uso (Extraído do Código) |  
      |---------------|-------------|--------------------------------------|  
      | `MAX_SIZE`    | `int = 100` | Limite máximo para iterações.        |  

   ## 5. **Fluxo de Execução**  
      - [Ordem de chamadas de funções, condições `if __name__ == "__main__"`, etc.]  

   ## 6. **Dependências Críticas**  
      - [Listar bibliotecas externas e versões mínimas, se especificadas no código.]  

   ## 7. **Observações**  
      - [Erros conhecidos, TODOs ou avisos documentados no próprio arquivo.]  
   ```  

2. **Regras Estritas:**  
   - **Proibido extrapolar:** Se um trecho for ambíguo, use: *"[Informação incompleta: não há contexto no arquivo.]"*.  
   - **Comentários/Docstrings:** Convertidos literalmente para notas no MD.  
   - **Nenhuma adição externa:** Não explique conceitos gerais de Python (ex.: "`def` cria uma função").  

---  

### **Exemplo de Saída Esperada (Baseado em Código Simples):**  
```markdown
# Análise Técnica: `calculadora.py`  

## 1. Metadados  
- **Autor:** João Silva (extraído do comentário linha 1).  

## 2. Propósito Principal  
- Implementa operações básicas (soma, subtração) para uso em CLI.  

## 3. Estrutura do Código  
### **Imports**  
```python
import sys  
```  
**Finalidade:** `sys`: Manipulação de argumentos da linha de comando.  

### **Função `somar`**  
```python
def somar(a: float, b: float) -> float:  
    return a + b  
```  
- **Parâmetros:**  
  - `a`: float | Primeiro operando.  
  - `b`: float | Segundo operando.  
- **Lógica:** Retorna a soma dos dois valores de entrada.  
```  

---  

**Nota Final:**  
"Se o arquivo estiver vazio ou incompleto, retorne apenas: *[Arquivo não contém informações analisáveis.]*"