# Instruções para IA Criar Rede Neural do Processo "CriticoInformacaoRecebida"

Com base no diagrama UML fornecido, aqui estão as instruções detalhadas para criar uma rede neural que implemente o processo "Python CriticoInformacaoRecebida":

## Instruções para a IA:

1. **Objetivo Principal**:
   - Criar uma rede neural que atue como crítico de informações recebidas, validando arquivos e instruções de objetivo conforme o fluxo descrito no UML

2. **Arquitetura da Rede Neural**:
   - Implementar um modelo híbrido com:
     * Camadas CNN para processamento de documentos (imagens/textos PDF)
     * Camadas LSTM/Transformer para análise sequencial de instruções
     * Módulo de atenção para identificar contradições
     * Camada densa final para decisão binária (aceitar/rejeitar)

3. **Funções Críticas a Implementar**:
   ```python
   def validar_instrucao(texto_instrucao):
       # Analisar se a instrução tem:
       # - Objetivo claro
       # - Terminação definida
       # - Contexto explícito (indivíduo, local, entidade, disciplina)
       return bool_valido, erros_encontrados

   def verificar_contradicoes(texto_arquivo, instrucao):
       # Comparar regras no arquivo com a instrução
       # Identificar paradoxos ou conflitos lógicos
       return contradicoes, nivel_severidade

   def avaliar_fidelidade(texto_arquivo):
       # Verificar consistência interna do documento
       # Checar equilíbrio de argumentos (se aplicável)
       return score_fidelidade, pontos_fracos
   ```

4. **Fluxo de Processamento**:
   1. Receber entrada combinada (arquivo + instrução)
   2. Extrair features textuais e estruturais
   3. Paralelizar:
      - Análise semântica da instrução
      - Verificação de contradições
      - Avaliação de fidelidade
   4. Combinar resultados para decisão final

5. **Critérios de Saída**:
   - Saída deve conter:
     * Decisão (aceitar/rejeitar)
     * Lista de erros encontrados (se aplicável)
     * Pontuação de confiança
     * Sugestões de correção (para casos rejeitados)

6. **Treinamento Recomendado**:
   - Usar dataset com:
     * Pares válidos/inválidos de instruções
     * Documentos com contradições conhecidas
     * Exemplos de quebras de fidelidade
   - Loss function: Binary Cross-Entropy + Regularização L2

7. **Integração com Sistema**:
   - Formato de saída compatível com o "SeparadorDeContexto"
   - Logs detalhados para feedback do usuário
   - Threshold ajustável para sensibilidade

8. **Otimizações Sugeridas**:
   - Pré-processamento com NLP para identificação de entidades
   - Cache de resultados para instruções similares
   - Mecanismo de auto-aprendizado com feedback do usuário

## Exemplo de Código Estrutural:
```python
class InformationCritic(nn.Module):
    def __init__(self):
        super().__init__()
        self.text_encoder = TransformerEncoder(...)
        self.contradiction_head = nn.Linear(...)
        self.validity_head = nn.Linear(...)
        
    def forward(self, documents, instructions):
        doc_features = self.text_encoder(documents)
        instr_features = self.text_encoder(instructions)
        
        # Cross-analysis between docs and instructions
        attention_weights = torch.matmul(doc_features, instr_features.T)
        contradiction_score = self.contradiction_head(attention_weights)
        validity_score = self.validity_head(attention_weights)
        
        return {
            'valid': validity_score > 0.5,
            'contradictions': contradiction_score,
            'rejection_reasons': self.generate_reasons(attention_weights)
        }
```

## Requisitos Não-Funcionais:
- Tempo de resposta < 2s para documentos de até 50 páginas
- Acurácia mínima de 92% na detecção de contradições
- Explicabilidade das decisões (modelo interpretável)

Esta rede neural deve se integrar perfeitamente com o fluxo mostrado no UML, recebendo entradas do armazenamento e enviando saídas validadas para o SeparadorDeContexto.