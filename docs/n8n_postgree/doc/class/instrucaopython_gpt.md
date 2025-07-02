Abaixo segue uma proposta de **Instrução Oficial para o Assistente IA**, organizada em blocos numerados, com pré-análise de possíveis conflitos e sugestão de conciliação, seguida da instrução final completa.

---

## 1. Detecção de possíveis regras contraditórias

1. **Janela de agendamento vs. consulta prévia**

   * **Regra A:** “Reservas só podem ser feitas entre 4 e 60 dias a partir de hoje.”
   * **Regra B:** No fluxo de consulta, não há menção de limitação de data—poderia o usuário consultar datas fora dessa janela?

2. **Timeout na resposta vs. pagamento em 5 dias**

   * **Regra C:** “Se o usuário demorar mais de 2 min para responder, encerrar fluxo.”
   * **Regra D:** “Pagamento deve ocorrer em até 5 dias após a reserva.”

> **Sugestão conciliatória**
>
> * Na etapa de **consulta**, aplique já a janela de 4–60 dias (Regra A) para ambas as ações (consulta e reserva), evitando dúvidas.
> * Separe claramente as janelas de **diálogo** (2 min por interação) e de **pagamento** (5 dias após geração de link), pois atuam em momentos distintos.

---

## 2. Sugestão de reconciliação final

1. **Unificar janela de datas**

   * Ao perguntar “Qual data…?”, já filtrar e recusar datas fora de 4–60 dias, tanto para consulta quanto para reserva.

2. **Isolar timeouts de diálogo**

   * Manter o timeout de 2 min para cada pergunta/resposta.
   * Manter o prazo de 5 dias apenas para a confirmação de pagamento, sem impactar o diálogo ativo.

---

## 3. Instrução Oficial para o Assistente IA

**Título:** Gerar classe Python de reserva via WhatsApp + n8n (WAHA)

**Prompt:**
Você é um assistente de IA que **gera código em Python** para implementar todo o fluxo de consulta e reserva de quiosques via WhatsApp, orquestrado pelo n8n com o nó WAHA. Baseie-se nas especificações abaixo e nos arquivos de fluxo anexos (`classdiagram.mmd`, `flowchart.mmd`, `sequenceDiagram.mmd`).

---

### 3.1 Contexto e Objetivo

1. Ouvir mensagens de WhatsApp via nó WAHA (n8n).
2. Processar intenções de **consulta** e **reserva** de 4 tipos de quiosque.

### 3.2 Pré-requisitos

* Conexão com PostgreSQL e tabelas:

  * `usuarios(celular, nome, …)`
  * `reservas(data DATE, quiosque_id INT, status TEXT, pagamento_link TEXT, criado_em TIMESTAMP)`
  * `logs_whatsapp(timestamp TIMESTAMP, celular TEXT, etapa TEXT, sucesso BOOLEAN, payload JSON)`

### 3.3 Dados Principais

* **Quiosques**:
  1 ⇒ Família
  2 ⇒ Salão de Jogos
  3 ⇒ Quadra
  4 ⇒ Campo Sintético

### 3.4 Regras de negócio

1. **Filtro de datas (4–60 dias)**

   * Toda data informada fora desse intervalo deve ser recusada já na consulta.
2. **Timeout de interação (2 min)**

   * Se o usuário demorar mais de 2 min para responder, envie mensagem de timeout e encerre o fluxo.
3. **Pagamento (5 dias)**

   * Após reserva provisória, gerar link e aguardar confirmação em até 5 dias.
   * Se pago → status `CONFIRMADA`; se não → `CANCELADA`.

### 3.5 Estrutura da classe Python

**Classe**: `QuisqueReservationBot`

1. **Atributos**

   * `db_conn` (conexão ao PostgreSQL)
   * `whatsapp_client` (cliente WAHA)
2. **Métodos principais**

   1. `listen()`

      * Inicia loop de escuta no webhook do WAHA.
   2. `handle_message(message)`

      * Extrai `celular`, `intenção` e chama `validate_user()` ou `process_reservation()`.
   3. `validate_user(celular)` → Boolean

      * Verifica existência em `usuarios`.
   4. `query_availability(data, quiosque_id)` → Boolean

      * Checa `reservas` para a data e quiosque.
   5. `make_reservation(celular, data, quiosque_id)` → `pagamento_link`

      * Insere reserva provisória e retorna link de pagamento.
   6. `confirm_payment(reserva_id)`

      * Observa confirmação de pagamento (webhook/polling) e atualiza status.
   7. `log_step(celular, etapa, sucesso, payload)`

      * Grava em `logs_whatsapp`.
   8. Métodos auxiliares para timeout de diálogo e envio de mensagens-padrão.

### 3.6 Fluxo de uso (baseado nos diagramas)

1. **Sequência UML**: seguir `sequenceDiagram.mmd`.
2. **Fluxograma**: para organização genérica do estado de cada interação.
3. **Diagrama de classes**: mapeia entidades do sistema.

---

**Exemplo de cabeçalho de arquivo gerado** (Mermaid):

```python
# -*- coding: utf-8 -*-
"""
Classe: QuisqueReservationBot
Geração automática pelo Assistente IA em [DATA]
Fluxos: classdiagram.mmd, flowchart.mmd, sequenceDiagram.mmd
"""
```

**Perguntas e Respostas Internas**

1. **P:** Como trato datas inválidas?
   **R:** Rejeitar imediatamente com “Reservas só entre 4 e 60 dias.”
2. **P:** E se usuário não responder?
   **R:** Após 2 min, enviar “Tempo esgotado…” e encerrar.
3. **P:** Onde gravar logs?
   **R:** Em `logs_whatsapp`, a cada método chamado.

---

Com isso, o Assistente IA terá tudo o que precisa para **gerar a classe Python** completa, estruturada, conforme os arquivos de fluxo e as regras de negócio consolidadas.
