# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando cada etapa conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).
- **N.avaliacao_continua/__init__.py**: Expõe a classe principal `AvaliacaoContinua` do módulo `avaliacao_continua.py`.
- **N.avaliacao_continua/avaliacao_continua.py**:
  - **Dependências externas**:
    - `rouge_score.rouge_scorer`: cálculo de ROUGE-L.
    - `bert_score.BERTScorer`: cálculo de BERTScore.
    - (Opcional) LLM para avaliação automática (parâmetro `llm_judge`).
    - `logging`: instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.

- **Fluxo de dados**:
  - Recebe resultados do LLM com RAG (lista de dicts com query, resposta, etc).
  - Avalia respostas automaticamente (ROUGE, BERTScore), via LLM-as-a-judge e stub para avaliação humana.
  - Retorna avaliações agregadas para cada item.

---

## 2. Descrição por Arquivo

### N.avaliacao_continua/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `AvaliacaoContinua`
- **Dependências internas**: Importa de `.avaliacao_continua`
- **Dependências externas**: Nenhuma

### N.avaliacao_continua/avaliacao_continua.py

- **Propósito principal**: Implementa avaliação contínua de respostas do sistema, usando métricas automáticas, LLM-as-a-judge e stub para avaliação humana.
- **Classe exportada**: `AvaliacaoContinua`
  - **__init__**: 
    - Parâmetros: instâncias de LLM judge, ROUGE scorer, BERT scorer, nível de log.
    - Instancia scorers e logger.
  - **_stub_llm_judge**:
    - Função stub para simular avaliação LLM-as-a-judge.
  - **avaliar_automatico**:
    - Calcula ROUGE-L e BERTScore entre referência e resposta.
  - **avaliar_llm_judge**:
    - Gera prompt para avaliação LLM-as-a-judge e retorna avaliação.
  - **avaliar_humano**:
    - Stub para avaliação humana (integração futura).
  - **run**:
    - Recebe lista de resultados do LLM com RAG e, opcionalmente, referências.
    - Para cada item, executa avaliação automática, LLM-as-a-judge e humana.
    - Loga e retorna avaliações agregadas.
- **Dependências externas**: `rouge_score`, `bert_score`, `logging`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando resultados do LLM com RAG para a etapa de avaliação contínua.
2. Instancia-se `AvaliacaoContinua` (com ou sem LLM judge/scorers customizados).
3. Chama-se o método `run(resultados_llmrag, referencias)`:
   - Para cada item:
     - Extrai query, resposta e referência.
     - Executa avaliação automática (ROUGE, BERTScore) se referência disponível.
     - Executa avaliação LLM-as-a-judge.
     - Executa avaliação humana (stub).
     - Loga avaliação.
   - Retorna lista de avaliações agregadas.
4. Resultados podem ser usados para monitoramento, ajuste de modelos e ciclo de melhoria contínua.
