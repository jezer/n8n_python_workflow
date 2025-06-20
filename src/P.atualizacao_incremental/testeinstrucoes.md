# INSTRUCOES_TESTES.md

## 1. Para cada módulo

### P.atualizacao_incremental/atualizacao_incremental.py

- [ ] **Pré-condições para teste**
  - Python 3.8+ instalado
  - Dependências: `numpy`, `faiss`, `logging`
  - Embeddings antigos, novos dados, consultas e ground-truth disponíveis (arrays numpy compatíveis)

- [ ] **Entradas válidas**
  - `embeddings_antigos`: np.ndarray (n x d)
  - `novos_dados`: np.ndarray (m x d)
  - `consultas`: np.ndarray (q x d)
  - `ground_truth`: np.ndarray (q,)
  - Versões: strings (ex: "001", "002")

- [ ] **Entradas inválidas**
  - Arrays vazios ou com dimensões incompatíveis
  - Tipos errados (ex: listas ao invés de np.ndarray)
  - Versões não informadas ou inválidas

- [ ] **Comportamentos esperados**
  - Embeddings são atualizados, normalizados e salvos corretamente
  - Recall@k é calculado antes e depois da atualização
  - Rollback é executado se recall cair mais que o threshold
  - Logs informam progresso, recall e rollback
  - Retorno é um dict com status e métricas de recall

- [ ] **Mockar (Simular) quais dependências**
  - FAISS: pode ser substituído por stub para testes rápidos
  - Sistema de arquivos: pode ser simulado para testar versionamento e rollback

## 2. Casos de Teste Sugeridos

- **Happy Path (Caminho ideal)**
  - Embeddings antigos e novos dados compatíveis resultam em atualização, cálculo de recall e status "atualizado"

- **Edge Cases (Casos extremos)**
  - Recall novo menor que antigo por mais de 5% (status "rollback")
  - Arrays de entrada vazios (deve lançar erro ou logar aviso)
  - Dimensões incompatíveis (deve lançar erro claro)
  - Versão de arquivo já existente (deve sobrescrever ou logar)

- **Failure Modes (Modos de falha)**
  - Falha ao salvar ou carregar embeddings (deve ser tratada e logada)
  - Falha ao calcular recall (deve ser tratada e logada)
  - Tipos de entrada errados: deve lançar erro claro
