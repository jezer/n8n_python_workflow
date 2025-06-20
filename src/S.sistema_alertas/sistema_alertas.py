import logging
from typing import List, Dict, Any, Optional
import smtplib
from email.message import EmailMessage

class SistemaAlertas:
    """
    Sistema de alertas automáticos baseado em detecção de anomalias do dashboard.
    Pode enviar alertas por log, e-mail ou integração externa.
    """

    def __init__(
        self,
        email_alerta: Optional[str] = None,
        smtp_server: str = "localhost",
        smtp_port: int = 25,
        log_level: int = logging.INFO
    ):
        self.email_alerta = email_alerta
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("SistemaAlertas")

    def analisar_anomalias(self, metricas: Dict[str, Any], anomalias: List[Dict[str, Any]]) -> List[str]:
        """
        Analisa as anomalias e gera mensagens de alerta.
        """
        alertas = []
        if anomalias:
            for anomalia in anomalias:
                msg = f"Anomalia detectada: {anomalia}"
                alertas.append(msg)
                self.logger.warning(msg)
        if metricas.get("recall@k", 1.0) < 0.7:
            msg = f"Alerta: Recall@k abaixo do limiar! Valor atual: {metricas.get('recall@k'):.2f}"
            alertas.append(msg)
            self.logger.warning(msg)
        return alertas

    def enviar_email(self, assunto: str, corpo: str):
        """
        Envia alerta por e-mail (stub, ajuste SMTP conforme necessário).
        """
        if not self.email_alerta:
            self.logger.info("E-mail de alerta não configurado.")
            return
        msg = EmailMessage()
        msg.set_content(corpo)
        msg["Subject"] = assunto
        msg["From"] = "alerta@pipeline.com"
        msg["To"] = self.email_alerta
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.send_message(msg)
            self.logger.info(f"Alerta enviado para {self.email_alerta}")
        except Exception as e:
            self.logger.error(f"Erro ao enviar e-mail de alerta: {e}")

    def run(self, relatorio_dashboard: Dict[str, Any]):
        """
        Executa o sistema de alertas com base no relatório do dashboard.
        """
        metricas = relatorio_dashboard.get("metricas", {})
        anomalias = relatorio_dashboard.get("anomalias", [])
        alertas = self.analisar_anomalias(metricas, anomalias)
        if alertas and self.email_alerta:
            self.enviar_email(
                assunto="Alerta do Pipeline de IA",
                corpo="\n".join(alertas)
            )
        return alertas