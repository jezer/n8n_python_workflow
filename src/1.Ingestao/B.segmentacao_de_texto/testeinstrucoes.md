# Instruções para Testes — Segmentação de Texto

## 1. Para cada módulo

### B.segmentacao_de_texto/segmentacao.py

- [ ] **Pré-condições para teste**
  - Disponibilidade de textos/documentos de entrada.
  - Modelos de IA treinados (ex: BERTimbau) disponíveis.
  - Ambiente Python com dependências instaladas.

- [ ] **Entradas válidas**
  - Lista de documentos/textos estruturados.
  - Textos com diferentes formatos (parágrafos, listas, etc).

- [ ] **Entradas inválidas**
  - Documentos vazios.
  - Textos corrompidos ou com encoding inválido.

- [ ] **Comportamentos esperados**
  - Segmentação correta dos textos.
  - Fallback para heurísticas quando IA não for conclusiva.
  - Logging das decisões de segmentação.

- [ ] **Mockar (Simular) quais dependências**
  - Classificador IA (ex: BERTimbau).
  - Funções de logging.

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Documentos bem formatados são segmentados corretamente.

- **Edge Cases (Casos extremos)**
  - Documentos com apenas um parágrafo.
  - Textos com muitos rodapés ou seções ambíguas.

- **Failure Modes (Modos de falha)**
  - Falha ao carregar modelo IA.
  - Texto com encoding inválido.
  - Exceções não tratadas durante segmentação.