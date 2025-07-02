Abaixo está um **fluxo completo** e aprimorado para a construção de uma instrução (“prompt”) de IA, organizado em etapas e blocos, inspirado na sua imagem e incluindo todos os pontos-chave de prompt engineering:

---

## 1. Definição de Meta e Papel

1. **Objetivo**

   * O que você quer que a IA faça? (e.g. “Resumir artigos acadêmicos em até 5 parágrafos”.)
2. **Papel do Assistente**

   * Descreva quem a IA deve ser: tom, nível de detalhe, voz (e.g. “Você é um analista sênior de dados, objetivo e direto, escrevendo em português formal.”)

## 2. Contexto e Histórico

1. **Contexto Geral**

   * Informações de fundo necessárias (e.g. “Estes artigos tratam de RAG e LangChain.”)
2. **Fontes ou Dados**

   * Indique arquivos, links ou variáveis de entrada (e.g. `arquivo_texto`, `resumo_previo`, `max_paragraphs`).

## 3. Parâmetros do Modelo

* **Modelo**: `gpt-3.5-turbo` (ou outro)
* **Max Tokens**: `1024`
* **Temperature**: `0.7`
* **Top P**: `1.0`
* **Frequency Penalty**: `0.0`
* **Presence Penalty**: `-2.0`

## 4. Variáveis Dinâmicas

```yaml
variables:
  max_paragraphs: 30
  domain: “[área do conhecimento]”
  tone: “[formal|informal]”
  language: “[pt|en]”
```

## 5. Stop Sequences

* Sequências que indicam ao modelo onde parar (e.g. `“###”`, `"FIM"` ou `"shhh"`).

## 6. Estrutura de Blocos de Mensagens

| Bloco                            | Objetivo                                                       | Exemplo de Conteúdo                                                         |
| -------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **System Message**               | Instruções globais que definem regras e limites                | “Você só deve responder dentro do escopo indicado. Não invente fatos.”      |
| **User – Tarefa**                | Descrição clara da tarefa a ser executada                      | “Resuma o texto abaixo em até {{max\_paragraphs}} parágrafos.”              |
| **User – Contexto**              | Detalhamento do contexto e público-alvo                        | “Público: gestores de TI sem background técnico.”                           |
| **User – Restrições**            | Limitações e proibições (tonalidade, formato, ética)           | “Não use listas numeradas. Mantenha parágrafos curtos (< 3 linhas).”        |
| **User – Instruções Detalhadas** | Passo-a-passo ou critérios de como estruturar a resposta       | “1. Introdução breve; 2. Desenvolvimento com 3 pontos-chave; 3. Conclusão.” |
| **User – Exemplos I/O**          | Amostras de input e output para guiar o modelo                 | “Input: ‘Texto sobre RAG’ → Output: ‘Resumo em 3 frases…’”                  |
| **User – Prompt de Saída**       | Como finalizar o prompt para a IA – geralmente uma única linha | “Agora, gere o resumo.”                                                     |

## 7. Critérios de Qualidade e Avaliação

* **Métricas**: coerência, completude, concisão, fidelidade ao original.
* **Checks**: “Se a resposta extrapolar {{max\_paragraphs}}, corte automaticamente no parágrafo final.”

## 8. Tratamento de Erros e Exceções

* O que fazer se faltar contexto ou dados (“Se o texto for vazio, peça mais informações: ‘Por favor, forneça o texto a ser resumido.’”).
* Regras de fallback (“Em caso de dúvida, responda pedindo esclarecimento.”).

## 9. Perguntas de Esclarecimento

* “Caso algo não esteja claro, pergunte: ‘Você quer foco em qual seção do texto?’”.

## 10. Iteração e Aprendizado

* Instruções para refinar o prompt conforme feedback:

  1. Colete comentários do usuário.
  2. Ajuste temperatura e penalidades.
  3. Reprovoque a IA com a versão corrigida do prompt.

---

### 📋 **Template Consolidado**

```yaml
# Parâmetros do Modelo
model: gpt-3.5-turbo
max_tokens: 1024
temperature: 0.7
top_p: 1.0
frequency_penalty: 0.0
presence_penalty: -2.0

variables:
  max_paragraphs: 30
  domain: "[área do conhecimento]"
  tone: "[formal|informal]"
  language: "[pt|en]"

stop_sequences:
  - "###"
  - "FIM"
  - "shhh"

messages:
  - role: system
    content: >
      Você é um [papel do assistente]. 
      Siga estritamente as regras e não saia do escopo definido.

  - role: user
    name: tarefa
    content: >
      Tarefa: Resuma o texto abaixo em até {{max_paragraphs}} parágrafos.

  - role: user
    name: contexto
    content: >
      Contexto: Público-alvo = gestores de TI sem background técnico.

  - role: user
    name: restricoes
    content: >
      Restrições:
      • Não use listas numeradas.
      • Parágrafos com no máximo 3 linhas.
      • Não inclua links.

  - role: user
    name: instrucoes
    content: >
      Instruções Detalhadas:
      1. Parágrafo de abertura com uma frase.
      2. Desenvolva 3 pontos-chave do texto.
      3. Conclua com recomendação prática.

  - role: user
    name: exemplos
    content: >
      Exemplo I/O:
      Input: “Texto sobre RAG em LangChain…”
      Output Esperado: “Resumo em 3 frases, destacando…”
  
  - role: user
    name: prompt_final
    content: >
      Agora, gere o resumo.

```

—
Use este **template** como base e adapte cada bloco às suas necessidades específicas: defina claro o objetivo, o público, as restrições, forneça exemplos, e ajuste parâmetros do modelo até atingir o resultado desejado.
