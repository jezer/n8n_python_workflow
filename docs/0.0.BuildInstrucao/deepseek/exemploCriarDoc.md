**OBJETIVO**
Preciso que Gere um prompt para avaliar um arquivo python, e queum documento.md explicado detalhadamente o arquivo .py.

Eu preciso que conste no prompt estes parametros:

*(Máxima fidelidade às fontes, sem criatividade ou extrapolação)*  

| Parâmetro        | Configuração | Justificativa |
|------------------|-------------|---------------|
| **Modelo**       | Modelos com melhor compreensão contextual. |
| **Temperatura**  | **0.1**     | Quase determinístico, minimiza invenções. |
| **Top P**        | **0.3**     | Amostra apenas tokens mais prováveis (baseados no contexto fornecido). |
| **Freq. Penalty**| **1.0**     | Penaliza repetição de termos incomuns nos arquivos. |
| **Pres. Penalty**| **1.5**     | Evita devaneios ou adições não contidas nos materiais. |

  
*"Sua resposta deve ser extraída exclusivamente dos arquivos anexados. "*