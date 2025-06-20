# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Orquestra o pipeline, chamando cada etapa conforme o fluxo do [`fluxo.mmd`](../docs/fluxo.mmd).
- **J.metadados_enriquecidos/__init__.py**: Expõe a classe principal `MetadadosEnriquecidos` do módulo `metadados_enriquecidos.py`.
- **J.metadados_enriquecidos/metadados_enriquecidos.py**:
  - **Dependências externas**:
    - `spacy`: para NER customizado (modelo transformer).
    - `logging`: instrumentação e logs.
    - `typing`: tipagem estática.
  - **Dependências internas**:
    - Função `get_supabase_client` (não definida no arquivo, depende de implementação externa).
    - Integração com grafo de conhecimento (parâmetro opcional `grafo`).
- **Fluxo de dados**:
  - Recebe documentos (com campos como `conteudo`, `pergunta_gerada`, `resposta_gerada`).
  - Extrai entidades nomeadas via spaCy.
  - Faz linking dessas entidades com entidades do grafo (se fornecido).
  - Loga todos os metadados extraídos.
  - Salva cada metadado no Supabase.

---

## 2. Descrição por Arquivo

### J.metadados_enriquecidos/__init__.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `MetadadosEnriquecidos`
- **Dependências internas**: Importa de `.metadados_enriquecidos`
- **Dependências externas**: Nenhuma

### J.metadados_enriquecidos/metadados_enriquecidos.py

- **Propósito principal**: Implementa extração de metadados via NER customizado, linking com entidades do grafo e persistência no Supabase.
- **Classe exportada**: `MetadadosEnriquecidos`
  - **__init__**: 
    - Parâmetros: modelo spaCy, entidades do grafo (opcional), nível de log.
    - Instancia pipeline spaCy e logger.
  - **extrair_metadados**:
    - Extrai entidades nomeadas do texto usando spaCy.
  - **linking_entidades**:
    - Faz linking das entidades extraídas com entidades do grafo.
  - **salvar_no_supabase**:
    - Salva metadados em tabela do Supabase (depende de função externa `get_supabase_client`).
  - **run**:
    - Pipeline principal: recebe lista de documentos, extrai e enriquece metadados, faz linking, loga e salva no Supabase.
    - Se grafo for fornecido, extrai entidades do grafo para linking.
    - Para cada documento, processa texto, extrai/linka metadados, loga e salva cada metadado no Supabase.
    - Retorna lista de documentos enriquecidos com metadados.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, passando documentos (ex: QAs, chunks, textos) para a etapa de metadados enriquecidos.
2. Instancia-se `MetadadosEnriquecidos` (com modelo spaCy e, opcionalmente, entidades do grafo).
3. Chama-se o método `run(documentos, grafo)`:
   - Se grafo for fornecido, extrai entidades para linking.
   - Para cada documento:
     - Seleciona texto de interesse (`pergunta_gerada`, `resposta_gerada` ou `conteudo`).
     - Extrai entidades nomeadas via spaCy.
     - Faz linking das entidades com o grafo.
     - Loga os metadados extraídos.
     - Salva cada metadado no Supabase.
     - Adiciona metadados ao documento.
   - Retorna lista de documentos enriquecidos.
4. Os documentos enriquecidos seguem para etapas seguintes do pipeline (ex: indexação, avaliação).
