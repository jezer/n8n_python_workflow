# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### J.metadados_enriquecidos/metadados_enriquecidos.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `spacy`, modelo spaCy transformer (`en_core_web_trf` ou similar), `logging`
  - Função `get_supabase_client` disponível e configurada (ou mockada)
  - Supabase acessível (ou mock)

- [ ] **Entradas válidas**
  - Lista de dicionários com campos `"conteudo"`, `"pergunta_gerada"` ou `"resposta_gerada"`
  - Grafo opcional (iterável de triplas)

- [ ] **Entradas inválidas**
  - Lista vazia
  - Dicionários sem os campos esperados
  - Textos vazios ou não textuais
  - Grafo malformado ou não iterável

- [ ] **Comportamentos esperados**
  - Entidades nomeadas são extraídas corretamente do texto
  - Linking com entidades do grafo é realizado (se fornecido)
  - Metadados extraídos são logados
  - Cada metadado é salvo no Supabase
  - Retorno é uma lista de documentos, cada um com chave `"metadados"` contendo lista de metadados enriquecidos

- [ ] **Mockar (Simular) quais dependências**
  - Função `get_supabase_client` (mock para não acessar Supabase real)
  - Conexão Supabase (mock para simular inserção)
  - Pipeline spaCy (pode ser substituído por stub para testes rápidos)

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Documentos com textos ricos em entidades resultam em metadados extraídos, linkados e salvos corretamente.

- **Edge Cases (Casos extremos)**
  - Documento sem entidades nomeadas (retorna lista vazia de metadados)
  - Documento sem campos `"conteudo"`, `"pergunta_gerada"` ou `"resposta_gerada"` (deve ser ignorado ou tratado)
  - Grafo não fornecido (linking não é realizado)
  - Grafo com entidades não presentes no texto (nenhum metadado linkado)

- **Failure Modes (Modos de falha)**
  - Falha ao carregar modelo spaCy (deve ser tratada e logada)
  - Falha ao conectar ou inserir no Supabase (deve ser tratada e logada)
  - Lista de entrada não é lista (deve lançar erro claro)
  - Grafo malformado (deve lançar erro claro)
