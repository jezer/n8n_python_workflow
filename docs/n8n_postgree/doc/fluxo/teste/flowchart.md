
%% Flowchart – Lógica de Decisões e Processos
flowchart TD
    %% Instrução IA: Início do fluxograma
    Start(["Início"])

    %% Instrução IA: Receber mensagem via WAHA
    ReceiveMsg(["Recebe mensagem"])
    Start --> ReceiveMsg

    %% Instrução IA: Verificar cadastro do usuário
    ReceiveMsg --> |não| AskRegister{"Usuário cadastrado?"}
    AskRegister -->|Não| MsgRegister["Enviar: 'Cadastre-se'"] --> End1(["Fim"])
    AskRegister -->|Sim| NextAction

    %% Instrução IA: Decidir intenção do usuário
    NextAction{"Intenção = Consulta ou Reserva?"}
    NextAction -->|Consulta| Consulta
    NextAction -->|Reserva| Reserva

    %% Subfluxo Consulta
    Consulta(["Pergunta data/quiosque"])
    Consulta --> CheckRes{"Verifica reserva já existente?"}
    CheckRes -->|Ocupado| MsgBusy["'Já reservado'"] --> End2(["Fim ou novo ciclo"])
    CheckRes -->|Disponível| MsgFree["'Disponível'"] --> End2

    %% Subfluxo Reserva
    Reserva(["Verifica janela 4–60 dias"])
    Reserva --> WindowCheck
    WindowCheck -->|Fora| MsgWindowErr["'Data fora da janela'"] --> End3(["Fim"])
    WindowCheck -->|Dentro| MakePend["Inserir reserva PENDENTE"]
    MakePend --> GenLink["Gerar link de pagamento"]
    GenLink --> MsgPending["Enviar link e mensagem provisória"] --> End3

    %% Processo paralelo: Timeout e Pagamento
    subgraph Paralelo
      direction LR
      Timeout["Timeout usuário (2 min)"] --> MsgTimeout["'Tempo excedido'"] --> End4(["Fim"])
      WaitPay["Verificação de pagamento (5 dias)"] --> UpdateStatus
      UpdateStatus{"Pago?"}
      UpdateStatus -->|Sim| Confirm["Atualiza para CONFIRMADA e notifica"]
      UpdateStatus -->|Não| Cancel["Atualiza para CANCELADA e notifica"]
    end
