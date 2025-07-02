Antes de apresentarmos a instrução final, identifiquei dois pontos que podem entrar em conflito:

1. **Amplitude de leitura vs. desempenho**

   * Ler “MUITAS pastas e arquivos” (item 6) pode sobrecarregar o processo, tornando-o lento e propenso a erros.
   * Ao mesmo tempo, espera-se “gerar muitos arquivos e refatorar muitos arquivos” (preocupação), o que intensifica essa carga.

2. **Geração de documentação x geração de artefatos finais**

   * Você quer tanto “gerar boas instruções para documentação” (itens 1 e 2)
   * Quanto “depois de ler documentação… gerar códigos e roteiros” (itens 3 e 4).
   * Se o fluxo de documentação for muito detalhado, pode atrasar a fase de geração de artefatos; se for muito resumido, pode faltar informação para a geração.

**Solução conciliatória proposta**
– **Pipeline em estágios**: dividir o processo em módulos encadeados, onde cada módulo recebe apenas o que precisa do anterior:

1. *Indexação seletiva* (escopo reduzido de pastas/arquivos)
2. *Documentação resumida* (visão geral + metadados)
3. *Geração de artefatos* (códigos, roteiros etc)
4. *Refinamento incremental* (caso falte contexto, volta ao módulo 2 para detalhar)

Assim, equilibramos performance e profundidade sem travar o pipeline.

---

## Instrução para IA: Uso Eficiente do gemini-cli

**Objetivo geral:** Orientar o assistente a orquestrar o gemini-cli de modo modular, garantindo qualidade na documentação e nos artefatos finais, sem sacrificar desempenho.

### 1. Passos Gerais do Pipeline

1. **Indexação Seletiva**
   1.1. Pergunta: *“Como identificar apenas os arquivos relevantes para o escopo atual?”*
   1.2. Resposta: Use `gemini-cli scan --pattern "<pasta|extensão>" --exclude "<pasta_excluir>"` para gerar um índice, filtrando por metadados (tamanho, data, tags).
2. **Geração de Documentação Resumida**
   2.1. Pergunta: *“Como gerar documentação de código e fluxos UML?”*
   2.2. Resposta: Use `gemini-cli doc code --output docs/code --format markdown --uml generate` e `gemini-cli doc flow --output docs/flow --template mermaid`.
3. **Produção de Artefatos Finais**
   3.1. Pergunta: *“Como gerar códigos a partir da documentação de API e classes?”*
   3.2. Resposta: Use `gemini-cli generate code --input docs/code --language python --output src/` para scaffolding inicial; em seguida, `gemini-cli refactor code --rules semaforo` para aplicar padrões.
   3.3. Pergunta: *“Como criar roteiros e apresentações de marketing de longo prazo?”*
   3.4. Resposta: Use `gemini-cli doc script --input docs/flow --style “long-term-marketing” --output content/scripts`, e `gemini-cli doc slides --template corporate --output content/slides`.
4. **Refinamento Incremental**
   4.1. Pergunta: *“E se faltar detalhes na documentação para gerar o artefato?”*
   4.2. Resposta: Detecte gaps com `gemini-cli validate docs/* --report gaps.json`; depois reexecute `doc` apenas nas seções indicadas.

### 2. Módulos Específicos e Q\&A

| Módulo                                     | Comando Exemplo                                                                  |
| ------------------------------------------ | -------------------------------------------------------------------------------- |
| **1. Indexação Seletiva**                  | `gemini-cli scan --pattern "src/**/*.py" --exclude "tests/**"`                   |
| **2. Doc. de Código & UML**                | `gemini-cli doc code --format markdown --uml`                                    |
| **3. Doc. de Roteiros & Treinamentos**     | `gemini-cli doc script --style "ethics, long-term" --output tutorials/`          |
| **4. Geração de Códigos & Artefatos**      | `gemini-cli generate code --input docs/code --language python`                   |
| **5. Refatoração em Lote**                 | `gemini-cli refactor project --rules performance, style`                         |
| **6. Busca em Pastas, Imagens e Arquivos** | `gemini-cli find --index-index.json --query "design patterns" --output results/` |

### 3. Boas Práticas e Ética

1. **Modularize** sempre em pequenos lotes para evitar sobrecarga.
2. **Versione** seus índices e documentos (use Git).
3. **Verifique** gaps antes de gerar artefatos finais.
4. **Respeite** a ética de marketing: conteúdo educativo, transparente e de valor a longo prazo.
5. **Automatize** testes de qualidade (linters, validadores de UML, spellcheck).

### 4. Priorização

1. **Desempenho** (Indexação seletiva)
2. **Clareza** (Documentação resumida mas completa)
3. **Qualidade** (Geração de artefatos com padrões)
4. **Escalabilidade** (Refinamento incremental)

---

Com este conjunto estruturado de perguntas e respostas, a IA terá um guia claro para usar o gemini-cli de forma eficiente, escalável e ética.
