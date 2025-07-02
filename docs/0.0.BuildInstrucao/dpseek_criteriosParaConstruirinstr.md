# Instrução Completa para Construção de Prompt de IA

Com base na imagem fornecida e expandindo seus conceitos, aqui está uma estrutura completa para construir instruções eficazes para IA:

## 1. Configurações do Modelo
- **Modelo**: Especificar (ex: GPT-4, Claude 3, Gemini 1.5)
- **Temperatura**: 
  - Valor recomendado: 0.7 (para equilíbrio criatividade/coerência)
  - Escala: 0 (determinístico) a 2 (altamente criativo)
- **Top P**: 
  - Valor recomendado: 0.9 
  - Escala: 0 a 1 (amostragem por núcleo)
- **Penalidade de Frequência**: 
  - Valor recomendado: 0.5 
  - Escala: -2 (encorajar repetição) a 2 (evitar repetição)
- **Penalidade de Presença**: 
  - Valor recomendado: 0.5
  - Escala: -2 a 2

## 2. Estrutura do Prompt
### Bloco de Sistema
- **Identificação**: Nome/ID do bloco (ex: Block#edb41c)
- **Função**: Definir papel da IA (ex: especialista, assistente criativo)
- **Regras**: 
  - Formato de saída esperado
  - Restrições ou diretrizes éticas
  - Estilo de linguagem preferido

### Bloco de Usuário
- **Tarefa Principal**: Descrição clara e concisa do objetivo
- **Contexto**: Informações relevantes para a tarefa
- **Exemplos**: (opcional) Demonstrações do formato esperado
- **Instruções Específicas**:
  - Passos a seguir
  - Métodos a aplicar
  - Critérios de qualidade

### Blocos Adicionais
- **Dados de Entrada**: 
  - Texto estruturado ou não estruturado
  - Dados tabulares se aplicável
- **Metadados**: 
  - Comprimento máximo (ex: 30 parágrafos)
  - Idioma preferido
  - Referências a utilizar

## 3. Elementos de Refinamento
- **Primer de Saída**: Frase inicial para guiar o modelo
- **Razores Filosóficos**: Princípios orientadores (ex: Navalha de Occam)
- **Variáveis Controláveis**: Parâmetros ajustáveis pelo usuário
- **Exemplos de Boas Respostas**: (opcional) Para fine-tuning

## 4. Template Completo de Exemplo

```
[Configurações]
Modelo: GPT-4
Temperatura: 0.7
Top P: 0.9
Freq. penalty: 0.5
Pres. penalty: 0.5

[Bloco de Sistema]
ID: Block#expert123
Você é um assistente especializado em filosofia e pensamento crítico. Suas respostas devem ser precisas, bem estruturadas e aplicar princípios lógicos. Evite especulações não fundamentadas.

[Bloco de Usuário]
Tarefa: Explique o conceito de "navalha de Occam" e aplique-o para analisar a seguinte afirmação: "O universo foi criado por uma inteligência superior que depois se tornou indetectável"

Instruções:
1. Defina o princípio em 1-2 frases
2. Aplique-o à afirmação fornecida
3. Avalie a validade do argumento
4. Sugira alternativas mais simples

Formato esperado:
- Definição: [texto]
- Análise: [texto]
- Avaliação: [texto]
- Alternativas: [lista]

[Variáveis]
max_paragraphs: 3
idioma: pt-BR
```

## 5. Melhores Práticas
1. Seja explícito sobre o formato desejado
2. Forneça exemplos quando possível
3. Balanceie detalhe com concisão
4. Especifique restrições claras
5. Inclua critérios de sucesso
6. Considere adicionar "pensar passo a passo" para tarefas complexas

Esta estrutura abrangente cobre todos os elementos essenciais para criar prompts eficazes, combinando os elementos visíveis na imagem com técnicas comprovadas de engenharia de prompts.