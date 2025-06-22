# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Ponto de entrada do pipeline, orquestra as etapas do fluxo definido em `fluxo.mmd`.
- **F.grafo_conhecimento/\_\_init\_\_.py**: Expõe a classe principal `GrafoConhecimento` do módulo `grafo_conhecimento.py`.
- **F.grafo_conhecimento/grafo_conhecimento.py**:
  - **Dependências externas**:
    - `rdflib`: manipulação e serialização de grafos RDF.
    - `logging`: instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**: Nenhuma explícita além do próprio pacote.

- **Fluxo de dados**:
  - Recebe documentos classificados da etapa anterior (E).
  - Extrai triplas (sujeito, predicado, objeto) de cada chunk classificado.
  - Normaliza entidades e monta o grafo RDF.
  - Permite exportação do grafo para arquivo.

---

## 2. Descrição por Arquivo

### F.grafo_conhecimento/\_\_init\_\_.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `GrafoConhecimento`
- **Dependências internas**: Importa de `.grafo_conhecimento`
- **Dependências externas**: Nenhuma

### F.grafo_conhecimento/grafo_conhecimento.py

- **Propósito principal**: Implementa a geração do grafo de conhecimento a partir de chunks classificados, extraindo triplas e montando um grafo RDF.
- **Classe exportada**: `GrafoConhecimento`
  - **__init__**: 
    - Parâmetros: namespace RDF, nível de log.
    - Instancia grafo RDF e logger.
  - **extrair_triplas**:
    - Extrai triplas do texto do chunk (stub: exemplo simples, pode ser substituído por modelo REBEL).
  - **normalizar_entidade**:
    - Normaliza nomes de entidades (exemplo: "Python3" → "Python 3").
  - **adicionar_triplas_ao_grafo**:
    - Adiciona triplas extraídas ao grafo RDF.
  - **run**:
    - Pipeline principal: recebe lista de documentos (cada um com 'chunks_classificados'), extrai triplas de cada chunk e monta o grafo.
  - **exportar_rdf**:
    - Serializa e exporta o grafo RDF para arquivo.
- **Dependências externas**: `rdflib`, `logging`, `typing`.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando documentos classificados para a etapa de grafo de conhecimento.
2. Instancia-se `GrafoConhecimento`.
3. Chama-se o método `run(documentos)`:
   - Para cada documento:
     - Para cada chunk classificado:
       - Extrai triplas do texto do chunk.
       - Normaliza entidades.
       - Adiciona triplas ao grafo RDF.
   - Loga o número de triplas geradas.
   - Retorna o grafo RDF.
4. (Opcional) Chama-se `exportar_rdf` para salvar o grafo em arquivo.
5. O grafo pode ser utilizado por etapas posteriores (ex: geração de QA, enriquecimento de metadados).
