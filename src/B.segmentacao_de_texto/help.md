# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Ponto de entrada do pipeline, chama a etapa de segmentação após a ingestão de arquivos.
- **B.segmentacao_de_texto/segmentacao.py**: Responsável pela segmentação de texto, recebe dados da etapa de ingestão (`A.ingestao_de_arquivos`) e entrega para limpeza e normalização (`C.limpeza_normalizacao`).
- **B.segmentacao_de_texto/__init__.py**: Facilita a importação da função/classe principal de segmentação.
- **Dependências internas**: Recebe dados de `A.ingestao_de_arquivos`, entrega para `C.limpeza_normalizacao`.
- **Dependências externas**: Pode utilizar modelos de IA (ex: BERTimbau), bibliotecas de NLP (spaCy, NLTK), logging.

---

## 2. Descrição por Arquivo

### B.segmentacao_de_texto/__init__.py

- **Propósito principal**: Inicializa o módulo de segmentação, normalmente expondo a classe/função principal (ex: `SegmentadorUnificado`).
- **Funções/Classes exportadas**: Importa e expõe a principal função/classe de segmentação do arquivo `segmentacao.py`.
- **Dependências internas**: Importa de `segmentacao.py`.
- **Dependências externas**: Nenhuma.

### B.segmentacao_de_texto/segmentacao.py

- **Propósito principal**: Implementa a lógica de segmentação de texto.
- **Funções/Classes exportadas**:
  - Exemplo provável: `SegmentadorUnificado` (classe ou função).
  - Métodos para segmentar documentos, aplicar classificadores IA, fallback heurístico.
- **Dependências internas**: Pode importar utilitários, modelos treinados, logging.
- **Dependências externas**: Modelos de IA (BERTimbau), bibliotecas de NLP (spaCy, NLTK), logging.

---

## 3. Fluxo Executável

1. **main.py** executa o pipeline, iniciando pela ingestão de arquivos.
2. O resultado da ingestão é passado para a etapa de segmentação, que utiliza o módulo `B.segmentacao_de_texto`.
3. O método principal (ex: `SegmentadorUnificado.segmentar`) processa os textos:
   - Aplica classificador binário (ex: BERTimbau).
   - Se necessário, utiliza heurísticas (ex: padrões de rodapé).
   - Loga decisões para auditoria.
4. O resultado segmentado é passado para a próxima etapa (`C.limpeza_normalizacao`).

---