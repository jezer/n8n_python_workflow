# Documentação do Módulo Principal (main.py)

## 1. Propósito

O arquivo `main.py` atua como o orquestrador central do pipeline de processamento de dados. Ele coordena a execução sequencial de diversas etapas, desde a ingestão inicial de arquivos até a geração de insights, monitoramento e alertas. Seu principal objetivo é integrar os diferentes módulos do sistema, garantindo um fluxo de trabalho coeso e automatizado para o tratamento de informações.

## 2. Funcionalidades Principais

O `main.py` encapsula a lógica de chamada e encadeamento das seguintes etapas do pipeline:

*   **Ingestão de Arquivos (`etapa_ingestao`)**: Processa arquivos de um diretório especificado, convertendo-os para um formato padronizado (Markdown).
*   **Segmentação de Texto (`etapa_segmentacao`)**: Divide o conteúdo dos arquivos em segmentos menores para facilitar o processamento subsequente.
*   **Limpeza e Normalização (`etapa_limpeza`)**: Realiza a pré-processamento dos segmentos, removendo ruídos e padronizando o texto.
*   **Chunking Inteligente (`etapa_chunking`)**: Agrupa os segmentos limpos em "chunks" (pedaços) de informação coerentes.
*   **Classificação e Tagging (`etapa_classificacao`)**: Atribui categorias e tags aos chunks para organização e recuperação.
*   **Grafo de Conhecimento (`etapa_grafo_conhecimento`)**: Constrói um grafo de conhecimento a partir das informações processadas, identificando entidades e relações. Os dados são persistidos no Supabase.
*   **Geração de Perguntas e Respostas (QA) (`etapa_geracao_qa`)**: Gera pares de perguntas e respostas com base no grafo de conhecimento. Os QAs são persistidos no Supabase.
*   **Embeddings Especializados (`etapa_embeddings`)**: Cria representações vetoriais (embeddings) dos dados para facilitar buscas semânticas. Os embeddings são persistidos no Supabase.
*   **Indexação Vetorial (`etapa_indexacao`)**: Indexa os embeddings para permitir buscas eficientes em grandes volumes de dados.
*   **Metadados Enriquecidos (`etapa_metadados`)**: Adiciona metadados contextuais aos dados processados.
*   **Hybrid Retriever (`etapa_hybrid_retriever`)**: Combina diferentes estratégias de recuperação de informações para obter resultados mais relevantes.
*   **Reranking com Cross-Encoder (`etapa_reranking`)**: Reordena os resultados do retriever para melhorar a relevância.
*   **LLM com RAG (`etapa_llm_rag`)**: Utiliza Large Language Models (LLMs) com Retrieval Augmented Generation (RAG) para gerar respostas contextuais.
*   **Avaliação Contínua (`etapa_avaliacao`)**: Avalia a qualidade das respostas geradas pelo LLM. Os resultados da avaliação são persistidos no Supabase.
*   **Retriever Adaptativo (`etapa_retriever_adaptativo`)**: Ajusta as estratégias de recuperação com base no feedback da avaliação.
*   **Atualização Incremental (`etapa_atualizacao_incremental`)**: Gerencia a atualização de embeddings e índices de forma incremental.
*   **Otimização de Prompts (`etapa_otimizacao_prompts`)**: Otimiza os prompts utilizados pelos LLMs para melhorar o desempenho.
*   **Dashboard de Monitoramento (`etapa_dashboard`)**: Gera um dashboard para visualizar métricas e o desempenho do pipeline.
*   **Sistema de Alertas (`etapa_alertas`)**: Monitora o pipeline e gera alertas com base em condições pré-definidas.

O módulo também inclui funções para interação com o Supabase, como `get_supabase_client()` e `salvar_no_supabase()`, além de funções para criação de tabelas no banco de dados (`criar_tabela_triplas`, `criar_tabela_metadados`, etc.).

## 3. Estrutura e Fluxo de Execução

O `main.py` é executado a partir da linha de comando, recebendo o caminho da pasta a ser processada como argumento.

```python
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_da_pasta>")
        sys.exit(1)
    caminho_pasta = sys.argv[1]
    print(f"Iniciando pipeline de ingestão na pasta: {caminho_pasta}\n")
    pipeline = PipelineOrquestrador(caminho_pasta)
    pipeline.rodar()
```

A execução principal é delegada à classe `PipelineOrquestrador` (importada de `Orquestrador.py`), que gerencia a sequência de chamadas das etapas. As funções `etapa_X` definidas em `main.py` são as implementações concretas de cada passo do pipeline.

## 4. Dependências

O `main.py` importa diversos módulos de subpastas dentro de `src/`, cada um responsável por uma etapa específica do pipeline. Ele também depende das configurações do Supabase (`supabase_config.py`) e da classe `PipelineOrquestrador` (`Orquestrador.py`).

## 5. Como Usar

Para executar o pipeline, utilize o seguinte comando no terminal, substituindo `<caminho_da_pasta>` pelo diretório que contém os arquivos a serem processados:

```bash
python main.py <caminho_da_pasta>
```

**Exemplo:**

```bash
python main.py ./data/documentos
```