

%% Sequence Diagram – Fluxo de Consulta e Reserva
sequenceDiagram
    %% Instrução IA: Lifeline do Usuário iniciando interação
    participant Usuário
    participant WAHA_Node as "WAHA Node"
    participant n8n as "n8n Workflow"
    participant PG as "PostgreSQL"
    participant PagWebhook as "Webhook Poll Pagamento"

    %% 1. Usuário envia comando
    %% Instrução IA  Capturar intenção consulta  reservar
    Usuário->>WAHA_Node  "consulta  reservar"

    %% 2. WAHA encaminha para o workflow
    WAHA_Node->>n8n: repassa mensagem

    %% 3. Workflow valida cadastro
    n8n->>PG: SELECT * FROM usuarios WHERE celular=…
    alt não cadastrado
      %% Instrução IA: Notificar erro e encerrar
      PG-->>n8n: vazio
      n8n->>Usuário: "Por favor, cadastre-se primeiro."
      return
    end

    opt Consulta de disponibilidade
      %% Instrução IA: Pergunta data e quiosque
      n8n->>Usuário: "Qual data e quiosque?"
      Usuário-->>n8n: data/quiosque
      n8n->>PG: SELECT * FROM reservas WHERE data=… AND quiosque=…
      alt ocupado
        n8n->>Usuário: "Já reservado"
      else disponível
        n8n->>Usuário: "Disponível. Deseja reservar?"
      end
    end

    opt Reserva de nova data
      %% Instrução IA: Verificar janela de 4–60 dias
      n8n->>n8n: if data ∉ [hoje+4, hoje+60]
      alt fora da janela
        n8n->>Usuário: "Data fora da janela de reserva."
        return
      end
      %% Instrução IA: Criar reserva PENDENTE
      n8n->>PG: INSERT INTO reservas(status='PENDENTE', …)
      %% Instrução IA: Gerar link de pagamento
      n8n->>Usuário: "Aqui está seu link de pagamento: <link>"
    end

    par Verificação de Pagamento (até 5 dias)
      PagWebhook->>PG: consulta status
      alt pago
        PG-->>PagWebhook: status=PAID
        PagWebhook->>PG: UPDATE reservas SET status='CONFIRMADA'
        PagWebhook->>Usuário: "Reserva confirmada!"
      else não pago após 5 dias
        PagWebhook->>PG: UPDATE reservas SET status='CANCELADA'
        PagWebhook->>Usuário: "Reserva cancelada por falta de pagamento."
      end
    and Timeout Usuário (2 min)
      %% Instrução IA: Se sem resposta após 2 minutos
      n8n->>Usuário: "Tempo excedido. Por favor, reinicie."
    end
