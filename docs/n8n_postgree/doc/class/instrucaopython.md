

## Instrução IA para Gerar Classe Python

```python
"""
Classe principal para gerenciamento do sistema de reservas de quiosques via WhatsApp
Integra com WAHA e n8n conforme diagramas e fluxos fornecidos
"""

from datetime import datetime, timedelta
from enum import Enum
import json
from typing import Optional

class TipoQuiosque(Enum):
    """Enumeração dos tipos de quiosque disponíveis"""
    FAMILIA = 1
    SALAO = 2
    QUADRA = 3
    CAMPO = 4

class StatusReserva(Enum):
    """Enumeração dos status possíveis de uma reserva"""
    PENDENTE = 1
    CONFIRMADA = 2
    CANCELADA = 3

class ReservaQuiosque:
    def __init__(self, db_connector):
        """
        Inicializa a classe principal do sistema de reservas
        
        Args:
            db_connector: Objeto de conexão com o banco de dados PostgreSQL
        """
        self.db = db_connector
        self.JANELA_MINIMA_DIAS = 4
        self.JANELA_MAXIMA_DIAS = 60
        self.TIMEOUT_RESPOSTA = timedelta(minutes=2)
        self.PRAZO_PAGAMENTO = timedelta(days=5)
    
    def processar_mensagem(self, mensagem: str, celular: str) -> dict:
        """
        Método principal para processar mensagens recebidas via WhatsApp
        
        Args:
            mensagem: Texto da mensagem recebida
            celular: Número do remetente
            
        Returns:
            dict: Resposta a ser enviada ao usuário e ações necessárias
        """
        # Registrar log de entrada
        self._registrar_log(celular, "recebimento_mensagem", True, {"mensagem": mensagem})
        
        # 1. Verificar se usuário está cadastrado
        usuario = self._verificar_usuario(celular)
        if not usuario:
            return self._gerar_resposta("Desculpe, seu número não está cadastrado. Por favor, cadastre-se em nosso site antes de continuar.")
        
        # 2. Determinar intenção (consulta ou reserva)
        intencao = self._determinar_intencao(mensagem)
        
        # 3. Processar conforme intenção
        if intencao == "consulta":
            return self._processar_consulta(celular, mensagem)
        elif intencao == "reserva":
            return self._processar_reserva(celular, mensagem)
        else:
            return self._gerar_resposta("Não entendi seu pedido. Por favor, use 'consultar' ou 'reservar'.")
    
    def _verificar_usuario(self, celular: str) -> Optional[dict]:
        """Verifica se usuário está cadastrado no sistema"""
        try:
            usuario = self.db.query("SELECT * FROM usuarios WHERE celular = %s", (celular,))
            return usuario[0] if usuario else None
        except Exception as e:
            self._registrar_log(celular, "verificacao_usuario", False, {"erro": str(e)})
            return None
    
    def _determinar_intencao(self, mensagem: str) -> str:
        """Determina se a intenção do usuário é consulta ou reserva"""
        mensagem = mensagem.lower()
        if "consultar" in mensagem or "disponível" in mensagem:
            return "consulta"
        elif "reservar" in mensagem or "agendar" in mensagem:
            return "reserva"
        return "indeterminado"
    
    def _processar_consulta(self, celular: str, mensagem: str) -> dict:
        """Processa uma solicitação de consulta de disponibilidade"""
        # Implementar lógica de consulta conforme fluxograma
        pass
    
    def _processar_reserva(self, celular: str, mensagem: str) -> dict:
        """Processa uma solicitação de reserva de quiosque"""
        # Implementar lógica de reserva conforme fluxograma
        pass
    
    def _validar_janela_reserva(self, data: datetime) -> bool:
        """Valida se a data está dentro da janela permitida (4-60 dias)"""
        hoje = datetime.now()
        data_minima = hoje + timedelta(days=self.JANELA_MINIMA_DIAS)
        data_maxima = hoje + timedelta(days=self.JANELA_MAXIMA_DIAS)
        return data_minima <= data <= data_maxima
    
    def _gerar_link_pagamento(self, reserva_id: int) -> str:
        """Gera um link de pagamento único para a reserva"""
        # Implementar integração com gateway de pagamento
        return f"https://pagamento.exemplo.com/{reserva_id}"
    
    def _registrar_log(self, celular: str, etapa: str, sucesso: bool, payload: dict):
        """Registra um log de auditoria no banco de dados"""
        log_data = {
            "timestamp": datetime.now(),
            "celular": celular,
            "etapa": etapa,
            "resultado": "sucesso" if sucesso else "erro",
            "payload": json.dumps(payload)
        }
        self.db.insert("logs_whatsapp", log_data)
    
    def _gerar_resposta(self, texto: str, acoes: Optional[list] = None) -> dict:
        """Estrutura padrão para respostas ao usuário"""
        return {
            "texto": texto,
            "acoes": acoes or [],
            "timestamp": datetime.now()
        }
```

## Instruções Complementares para IA

1. **Implementação dos Métodos Faltantes**:
   - Complete os métodos `_processar_consulta` e `_processar_reserva` seguindo exatamente a lógica descrita nos fluxogramas e diagramas de sequência.

2. **Integração com Banco de Dados**:
   - A classe espera um objeto `db_connector` que deve ser adaptado para sua biblioteca de acesso a dados específica (SQLAlchemy, psycopg2, etc.)

3. **Tratamento de Erros**:
   - Adicione tratamento de erros robusto em todos os métodos que interagem com o banco de dados ou serviços externos.

4. **Padrões de Projeto**:
   - Considere implementar o padrão Strategy para os diferentes tipos de quiosque caso haja comportamentos específicos para cada tipo.

5. **Testes**:
   - Gere casos de teste unitários para cada método, especialmente para a validação da janela de agendamento e determinação de intenção.

6. **Extensibilidade**:
   - Projete a classe para ser facilmente extensível para novos tipos de quiosque ou regras de negócio.

7. **Documentação**:
   - Adicione docstrings detalhadas para cada método explicando parâmetros, retornos e comportamentos excepcionais.

Esta classe encapsula toda a lógica principal do sistema conforme descrito nos documentos fornecidos, seguindo as regras de negócio e fluxos especificados.