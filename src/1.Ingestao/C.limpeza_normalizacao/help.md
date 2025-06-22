# ANÁLISE.md

## 1. Mapa de Dependências

- **main.py**: Ponto de entrada do pipeline, orquestra todas as etapas do fluxo descrito em `fluxo.mmd`.
- **C.limpeza_normalizacao/\_\_init\_\_.py**: Expõe a classe `LimpezaNormalizacao` do módulo `limpeza_normalizacao.py`.
- **C.limpeza_normalizacao/limpeza_normalizacao.py**: Implementa a lógica de limpeza e normalização de textos, utilizada após a segmentação e antes do chunking.
- **Dependências internas**: 
  - Recebe documentos segmentados da etapa B (segmentação de texto).
  - Entrega documentos limpos para a etapa D (chunking inteligente).
- **Dependências externas**:
  - `re`, `unicodedata` (biblioteca padrão Python)
  - Tipagem (`List`, `Dict`, `Any`, `Optional`)

## 2. Descrição por Arquivo

### C.limpeza_normalizacao/\_\_init\_\_.py

- **Propósito principal**: Facilita a importação da classe principal do módulo.
- **Exporta**: `LimpezaNormalizacao`
- **Dependências internas**: Importa de `.limpeza_normalizacao`
- **Dependências externas**: Nenhuma

### C.limpeza_normalizacao/limpeza_normalizacao.py

- **Propósito principal**: Realiza limpeza e normalização de textos, removendo cabeçalhos/rodapés, normalizando encoding e filtrando lixo textual.
- **Classe exportada**: `LimpezaNormalizacao`
  - **Métodos**:
    - `__init__(classificador_binario=None)`: Permite injetar um classificador binário externo.
    - `remover_cabecalho_rodape(texto)`: Remove linhas suspeitas do início/fim do texto.
    - `normalizar_encoding(texto)`: Normaliza acentuação e encoding para UTF-8.
    - `detectar_lixo(texto)`: Usa classificador binário ou heurística para identificar lixo textual.
    - `run(documentos)`: Pipeline principal; recebe lista de documentos e retorna apenas os limpos.
- **Dependências internas**: Nenhuma
- **Dependências externas**: `re`, `unicodedata`, tipagem

## 3. Fluxo Executável

1. **main.py** executa o pipeline, iniciando pela ingestão e segmentação de arquivos.
2. O resultado da segmentação é passado para a etapa de limpeza:
   - Instancia-se `LimpezaNormalizacao` (opcionalmente com um classificador binário).
   - Chama-se o método `run(documentos)`, que:
     - Normaliza encoding de cada documento.
     - Remove cabeçalhos e rodapés.
     - Filtra documentos considerados lixo.
   - Retorna apenas documentos limpos e normalizados.
3. Os documentos limpos seguem para o chunking inteligente e demais etapas do pipeline.