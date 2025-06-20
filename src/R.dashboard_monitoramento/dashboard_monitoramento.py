import logging
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import os
import json
import datetime

class DashboardMonitoramento:
    """
    Dashboard de monitoramento do pipeline: métricas, tendências, logs e detecção de anomalias.
    """

    def __init__(self, output_dir: str = "./dashboard", log_level: int = logging.INFO):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger("DashboardMonitoramento")

    def agregar_metricas(self, resultados_avaliacao: List[Dict[str, Any]], recall: Optional[float] = None) -> Dict[str, Any]:
        """
        Agrega métricas principais do pipeline.
        """
        total = len(resultados_avaliacao)
        scores = [item.get("avaliacao_automatica", {}).get("rougeL", 0) for item in resultados_avaliacao]
        media_rouge = sum(scores) / total if total else 0
        metricas = {
            "total_respostas": total,
            "media_rougeL": media_rouge,
            "recall@k": recall,
            "data": datetime.datetime.now().isoformat()
        }
        self.logger.info(f"Métricas agregadas: {metricas}")
        return metricas

    def plotar_tendencia(self, historico_metricas: List[Dict[str, Any]], metrica: str = "media_rougeL"):
        """
        Plota tendência temporal de uma métrica.
        """
        datas = [m["data"] for m in historico_metricas]
        valores = [m.get(metrica, 0) for m in historico_metricas]
        plt.figure(figsize=(8, 4))
        plt.plot(datas, valores, marker="o")
        plt.title(f"Tendência: {metrica}")
        plt.xlabel("Data")
        plt.ylabel(metrica)
        plt.xticks(rotation=45)
        plt.tight_layout()
        caminho = os.path.join(self.output_dir, f"tendencia_{metrica}.png")
        plt.savefig(caminho)
        plt.close()
        self.logger.info(f"Gráfico salvo em {caminho}")

    def detectar_anomalias(self, historico_metricas: List[Dict[str, Any]], metrica: str = "recall@k", threshold: float = 0.1) -> List[Dict[str, Any]]:
        """
        Detecta quedas abruptas na métrica especificada.
        """
        anomalias = []
        valores = [m.get(metrica, 0) for m in historico_metricas]
        for i in range(1, len(valores)):
            if valores[i-1] - valores[i] > threshold:
                anomalias.append(historico_metricas[i])
        if anomalias:
            self.logger.warning(f"Anomalias detectadas: {anomalias}")
        return anomalias

    def gerar_relatorio(self, metricas: Dict[str, Any], anomalias: List[Dict[str, Any]]):
        """
        Gera relatório em JSON.
        """
        relatorio = {
            "metricas": metricas,
            "anomalias": anomalias
        }
        caminho = os.path.join(self.output_dir, "relatorio_dashboard.json")
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Relatório salvo em {caminho}")

    def run(self, resultados_avaliacao: List[Dict[str, Any]], recall: Optional[float] = None, historico_metricas: Optional[List[Dict[str, Any]]] = None):
        """
        Executa o dashboard: agrega métricas, plota tendências, detecta anomalias e gera relatório.
        """
        metricas = self.agregar_metricas(resultados_avaliacao, recall)
        historico = historico_metricas or [metricas]
        self.plotar_tendencia(historico, metrica="media_rougeL")
        self.plotar_tendencia(historico, metrica="recall@k")
        anomalias = self.detectar_anomalias(historico, metrica="recall@k")
        self.gerar_relatorio(metricas, anomalias)