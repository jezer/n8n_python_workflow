# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### C.limpeza_normalizacao/limpeza_normalizacao.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências padrão (`re`, `unicodedata`)
  - Opcional: classificador binário mockado

- [ ] **Entradas válidas**
  - Lista de dicionários com chave `"conteudo"` contendo textos variados (com e sem cabeçalho/rodapé, diferentes encodings, textos limpos e com lixo)

- [ ] **Entradas inválidas**
  - Lista vazia
  - Dicionários sem chave `"conteudo"`
  - Textos muito curtos ou só com caracteres especiais

- [ ] **Comportamentos esperados**
  - Textos são normalizados para UTF-8
  - Cabeçalhos e rodapés suspeitos são removidos
  - Textos considerados lixo são descartados
  - Retorno é uma lista apenas com documentos limpos

- [ ] **Mockar (Simular) quais dependências**
  - Classificador binário (objeto/função com método `predict(texto)`)

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Documentos com cabeçalho/rodapé e encoding misto são limpos corretamente e retornados

- **Edge Cases (Casos extremos)**
  - Documento só com cabeçalho/rodapé (deve ser removido)
  - Documento com menos de 30 caracteres (deve ser descartado)
  - Documento com muitos caracteres gráficos (deve ser descartado)
  - Dicionário sem chave `"conteudo"` (deve ser ignorado ou tratado)

- **Failure Modes (Modos de falha)**
  - Classificador binário lança exceção (deve ser tratado)
  - Texto com encoding inválido (deve ser normalizado ou descartado)
  - Lista de entrada não é lista (deve lançar erro claro)