# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando cada etapa conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).
- **O.retriever_adaptativo/__init__.py**: Expõe a classe principal `RetrieverAdaptativo` do módulo `retriever_adaptativo.py`.
- **O.retriever_adaptativo/retriever_adaptativo.py**:
  - **Dependências externas**:
    - `logging`: instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.
- **Fluxo de dados**:
  - Recebe avaliações do sistema (ex: saída do módulo N - Avaliação Contínua).
  - Identifica hard negatives (falsos positivos) com base em métricas automáticas.
  - Realiza fine-tuning do retriever usando hard negatives e exemplos positivos.
  - Permite early stopping e logging do processo.

---

## 2. Descrição por Arquivo

### O.retriever_adaptativo/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `RetrieverAdaptativo`
- **Dependências internas**: Importa de `.retriever_adaptativo`
- **Dependências externas**: Nenhuma

### O.retriever_adaptativo/retriever_adaptativo.py

- **Propósito principal**: Implementa fine-tuning adaptativo do retriever via active learning, focando em hard negatives identificados automaticamente.
- **Classe exportada**: `RetrieverAdaptativo`
  - **__init__**: 
    - Parâmetros: modelo do retriever (opcional), taxa de aprendizado, número máximo de épocas, early stopping, nível de log.
    - Instancia modelo (stub por padrão) e logger.
  - **_stub_model**:
    - Função stub para simular modelo de retriever.
  - **identificar_hard_negatives**:
    - Identifica falsos positivos (hard negatives) a partir das avaliações, usando thresholds de ROUGE e BERTScore.
  - **fine_tune**:
    - Realiza fine-tuning do retriever usando hard negatives e exemplos positivos (stub).
  - **run**:
    - Orquestra identificação de hard negatives e fine-tuning do retriever, retornando ambos os resultados.
- **Dependências externas**: `logging`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando avaliações do sistema (ex: saída do módulo N) para o `RetrieverAdaptativo`.
2. Instancia-se `RetrieverAdaptativo` (com modelo e parâmetros desejados).
3. Chama-se o método `run(avaliacoes, positive_examples)`:
   - Identifica hard negatives a partir das avaliações.
   - Realiza fine-tuning do retriever usando hard negatives e exemplos positivos.
   - Retorna dicionário com hard negatives identificados e resultado do fine-tuning.
4. Resultados podem ser usados para atualizar o retriever e monitorar melhorias no sistema.
