

## Instrução IA – Geração de Diagramas UML e Fluxograma

1. **Objetivo Geral**
   Orientar o assistente a criar, com notação UML e de fluxograma, três artefatos para o projeto de reservas via WhatsApp + n8n (WAHA).

2. **Diagrama de Classes**
   2.1. **Entidades principais** (cada uma vira uma classe):

   * **Usuário**: atributos `celular: String`, `nome: String`
   * **Quiosque**: atributos `id: Integer`, `tipo: Enum{Família, Salão, Quadra, Campo}`
   * **Reserva**: atributos `data: Date`, `quiosque_id: Integer`, `status: Enum{PENDENTE, CONFIRMADA, CANCELADA}`
   * **Pagamento**: atributos `reserva_id: Integer`, `link: URL`, `data_criacao: DateTime`, `data_pagamento: DateTime?`
   * **Log**: atributos `timestamp: DateTime`, `celular: String`, `etapa: String`, `resultado: String`, `payload: JSON`
     2.2. **Relações**:
   * `Usuário 1──* Reserva`
   * `Quiosque 1──* Reserva`
   * `Reserva 1──1 Pagamento`
   * Todos os eventos são auditados em `Log` (associação indireta).

3. **Diagrama de Sequência**
   3.1. **Lifelines**: `Usuário` → `WAHA Node` → `n8n Workflow` → `PostgreSQL` → `Webhook/Polling Pagamento` → `n8n Workflow` → `Usuário`.
   3.2. **Mensagens-chave** (ordem):

   1. `Usuário` envia “consulta” ou “reservar” via WAHA
   2. `WAHA Node` repassa ao `n8n Workflow`
   3. `n8n Workflow` consulta `PostgreSQL.usuarios`

      * Se não cadastrado → retorna mensagem de erro e fim
   4. Se “consulta”: solicita data/quiosque → consulta `PostgreSQL.reservas` → responde disponibilidade
   5. Se “reservar” confirmado e data entre 4–60 dias: insere `Reserva(status=PENDENTE)` → gera link → envia ao `Usuário`
   6. **Em paralelo**: `Webhook/Polling Pagamento` verifica pagamento em até 5 dias →

      * Se pago → atualiza `Reserva(status=CONFIRMADA)` → notifica
      * Se não pago → atualiza `Reserva(status=CANCELADA)` → notifica

4. **Diagrama de Fluxo (Flowchart)**
   4.1. **Início** → **Recebe mensagem**
   4.2. **Decisão**: Usuário cadastrado?

   * Não → Mensagem “cadastre-se” → Fim
   * Sim → Próximo
     4.3. **Decisão**: Intenção = Consulta ou Reserva?
   * Consulta → Pergunta data/quiosque → Verifica `reservas` →

     * Se ocupado → “já reservado” → Fim ou novo ciclo
     * Se disponível → “disponível” → Oferece reserva → Fim ou segue para reserva
   * Reserva → Verifica janela (4–60 dias) →

     * Fora da janela → Mensagem de erro → Fim
     * Dentro → Inserir `PENDENTE` → Gerar link → Mensagem provisória → Fim
       4.4. **Processo paralelo**:
   * **Timeout 2 min** em cada espera de resposta → Mensagem “tempo excedido” → Fim
   * **Verificação de pagamento (5 dias)** → Atualiza status → Notifica → Fim

5. **Regras Específicas e Restrições**
   5.1. Janela de agendamento única: **entre 4 e 60 dias** a partir da data atual.
   5.2. Reserva só é confirmada após pagamento em até **5 dias**; caso contrário, **cancela**.
   5.3. Timeout na resposta do usuário: **2 minutos** → cancelar etapa e informar.
   5.4. Auditar **todas** as transições em `logs_whatsapp`.

