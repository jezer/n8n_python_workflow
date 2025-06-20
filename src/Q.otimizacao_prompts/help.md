# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, podendo acionar o módulo de otimização de prompts conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).
- **Q.otimizacao_prompts/__init__.py**: Expõe a classe principal `OtimizacaoPrompts` do módulo `otimizacao_prompts.py`.
- **Q.otimizacao_prompts/otimizacao_prompts.py**:
  - **Dependências externas**:
    - `logging`: instrumentação e logs.
    - `random`: geração de valores aleatórios para stubs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.
- **Fluxo de dados**:
  - Recebe avaliações de prompts/resultados do pipeline (ex: saída da avaliação contínua).
  - Executa otimização de prompts via A/B test ou STaR.
  - Loga variações e impactos.
  - Retorna melhores templates/prompts para cada pergunta.

---

## 2. Descrição por Arquivo

### Q.otimizacao_prompts/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `OtimizacaoPrompts`
- **Dependências internas**: Importa de `.otimizacao_prompts`
- **Dependências externas**: Nenhuma

### Q.otimizacao_prompts/otimizacao_prompts.py

- **Propósito principal**: Implementa otimização de prompts via A/B test e STaR, com logging detalhado.
- **Classe exportada**: `OtimizacaoPrompts`
  - **__init__**: 
    - Parâmetros: lista de templates, cliente LLM (stub por padrão), avaliador (stub por padrão), nível de log.
    - Instancia logger, templates e dependências.
  - **_stub_llm**:
    - Função stub para simular resposta do LLM.
  - **_stub_avaliador**:
    - Função stub para simular avaliação da resposta.
  - **ab_test**:
    - Executa A/B test entre templates para uma pergunta, loga scores e retorna o melhor.
  - **star_optimization**:
    - Executa STaR (Self-Taught Reasoner): gera raciocínio intermediário, ajusta prompt, avalia impacto e loga.
  - **run**:
    - Recebe lista de avaliações/resultados, executa otimização de prompts para cada pergunta, retorna melhores resultados.
- **Dependências externas**: `logging`, `random`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando avaliações/resultados para o módulo de otimização de prompts.
2. Instancia-se `OtimizacaoPrompts` (com templates, LLM e avaliador desejados).
3. Chama-se o método `run(resultados_avaliacao, metodo)`:
   - Para cada pergunta:
     - Executa A/B test ou STaR conforme o método.
     - Loga templates, prompts, respostas e scores.
     - Seleciona e retorna o melhor template/prompt para cada pergunta.
4. Resultados podem ser usados para atualizar prompts do pipeline, logs e análise de impacto.
