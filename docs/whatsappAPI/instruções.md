# Classe Python para API do WhatsApp

Vou criar um passo a passo para duas classes Python: uma para receber mensagens e outra para enviar mensagens (incluindo botões) usando a API do WhatsApp.

## Pré-requisitos
1. Ter uma conta na plataforma de API do WhatsApp (como Twilio, WhatsApp Business API ou outra)
2. Ter as credenciais de acesso (SID, token, número de telefone, etc.)
3. Python instalado (recomendo 3.7+)
4. Biblioteca `requests` instalada (`pip install requests`)

## Classe para Receber Mensagens

```python
from flask import Flask, request, jsonify
import json

class WhatsAppReceiver:
    """
    Classe para receber mensagens do WhatsApp via webhook
    """
    
    def __init__(self, app=None, webhook_endpoint='/webhook', verify_token=None):
        """
        Inicializa o receiver
        :param app: Instância do Flask (opcional)
        :param webhook_endpoint: Endpoint para o webhook
        :param verify_token: Token para verificação (opcional)
        """
        self.app = app or Flask(__name__)
        self.webhook_endpoint = webhook_endpoint
        self.verify_token = verify_token
        self.setup_routes()
    
    def setup_routes(self):
        """Configura as rotas do Flask"""
        @self.app.route(self.webhook_endpoint, methods=['GET'])
        def verify_webhook():
            # Verificação do webhook (usado pelo WhatsApp)
            if request.args.get('hub.verify_token') == self.verify_token:
                return request.args.get('hub.challenge'), 200
            return "Token de verificação inválido", 403
        
        @self.app.route(self.webhook_endpoint, methods=['POST'])
        def handle_incoming_messages():
            """Processa mensagens recebidas"""
            data = request.get_json()
            
            if data and 'object' in data and data['object'] == 'whatsapp_business_account':
                entries = data.get('entry', [])
                for entry in entries:
                    changes = entry.get('changes', [])
                    for change in changes:
                        value = change.get('value', {})
                        messages = value.get('messages', [])
                        for message in messages:
                            self.process_message(message)
            
            return jsonify({'status': 'success'}), 200
    
    def process_message(self, message):
        """
        Processa uma mensagem individual
        :param message: Dicionário com os dados da mensagem
        """
        # Implemente sua lógica de processamento aqui
        sender_id = message['from']
        message_body = message['text']['body'] if 'text' in message else None
        message_type = message['type']
        
        print(f"Recebido de {sender_id}: {message_body} (Tipo: {message_type})")
        
        # Você pode adicionar mais lógica aqui para responder automaticamente, etc.
    
    def run(self, host='0.0.0.0', port=5000):
        """Inicia o servidor Flask"""
        self.app.run(host=host, port=port)
```

## Classe para Enviar Mensagens (incluindo botões)

```python
import requests
from typing import List, Dict, Optional

class WhatsAppSender:
    """
    Classe para enviar mensagens via API do WhatsApp
    """
    
    def __init__(self, base_url: str, api_key: str, phone_number_id: str):
        """
        Inicializa o sender
        :param base_url: URL base da API (ex: 'https://graph.facebook.com/v13.0/')
        :param api_key: Token de acesso da API
        :param phone_number_id: ID do número de telefone
        """
        self.base_url = base_url
        self.api_key = api_key
        self.phone_number_id = phone_number_id
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def send_text_message(self, recipient: str, message: str) -> Dict:
        """
        Envia uma mensagem de texto
        :param recipient: Número do destinatário (com código do país, ex: 5511999999999)
        :param message: Texto da mensagem
        :return: Resposta da API
        """
        url = f"{self.base_url}{self.phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()
    
    def send_buttons(
        self,
        recipient: str,
        header_text: Optional[str],
        body_text: str,
        footer_text: Optional[str],
        buttons: List[Dict[str, str]]
    ) -> Dict:
        """
        Envia mensagem com botões de interação
        :param recipient: Número do destinatário
        :param header_text: Texto do cabeçalho (opcional)
        :param body_text: Texto principal
        :param footer_text: Texto do rodapé (opcional)
        :param buttons: Lista de botões (ex: [{"id": "btn1", "title": "Opção 1"}, ...])
        :return: Resposta da API
        """
        url = f"{self.base_url}{self.phone_number_id}/messages"
        
        # Formata os botões para o padrão da API
        formatted_buttons = []
        for btn in buttons:
            formatted_buttons.append({
                "type": "reply",
                "reply": {
                    "id": btn.get("id"),
                    "title": btn.get("title")
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body_text
                },
                "action": {
                    "buttons": formatted_buttons
                }
            }
        }
        
        # Adiciona header se fornecido
        if header_text:
            payload["interactive"]["header"] = {
                "type": "text",
                "text": header_text
            }
        
        # Adiciona footer se fornecido
        if footer_text:
            payload["interactive"]["footer"] = {
                "text": footer_text
            }
        
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()
```

## Como Usar as Classes

### 1. Para Receber Mensagens

```python
# Configuração do receiver
receiver = WhatsAppReceiver(
    webhook_endpoint='/whatsapp_webhook',
    verify_token='SEU_TOKEN_DE_VERIFICACAO'
)

# Inicia o servidor
receiver.run(port=5000)
```

### 2. Para Enviar Mensagens

```python
# Configuração do sender
sender = WhatsAppSender(
    base_url='https://graph.facebook.com/v13.0/',
    api_key='SEU_TOKEN_DA_API',
    phone_number_id='SEU_ID_DE_NUMERO'
)

# Enviar mensagem de texto
response = sender.send_text_message(
    recipient='5511999999999',
    message='Olá, esta é uma mensagem de teste!'
)
print(response)

# Enviar mensagem com botões
buttons = [
    {"id": "btn1", "title": "Opção 1"},
    {"id": "btn2", "title": "Opção 2"},
    {"id": "btn3", "title": "Opção 3"}
]

response = sender.send_buttons(
    recipient='5511999999999',
    header_text="Menu Principal",
    body_text="Por favor, escolha uma opção:",
    footer_text="Obrigado por usar nosso serviço!",
    buttons=buttons
)
print(response)
```

## Observações Importantes

1. **Segurança**: Nunca exponha suas chaves de API no código. Use variáveis de ambiente ou um gerenciador de segredos.

2. **Plataforma específica**: Este exemplo é genérico. Você precisará adaptar conforme a plataforma de API do WhatsApp que está usando (Meta/Facebook, Twilio, etc.).

3. **Webhook**: Para receber mensagens, você precisa configurar um webhook na plataforma de API do WhatsApp apontando para seu servidor.

4. **Certificado SSL**: Para produção, seu servidor precisa de HTTPS com um certificado válido.

5. **Limites da API**: Verifique os limites de taxa e outros requisitos da plataforma que está usando.