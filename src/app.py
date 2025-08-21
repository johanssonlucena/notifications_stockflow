from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title=&quot;Notification Service&quot;, version=&quot;1.0.0&quot;)
class AlertRequest(BaseModel):
product_name: str
current_quantity: int
min_quantity: int
sku: str
timestamp: str = None
@app.get(&quot;/health&quot;)
async def health_check():
&quot;&quot;&quot;Endpoint de health check&quot;&quot;&quot;
return {&quot;status&quot;: &quot;healthy&quot;, &quot;timestamp&quot;: datetime.utcnow().isoformat()}
@app.post(&quot;/alert&quot;)

async def send_alert(alert: AlertRequest):
&quot;&quot;&quot;Endpoint para enviar alertas de estoque baixo&quot;&quot;&quot;
try:
if not alert.timestamp:
alert.timestamp = datetime.utcnow().isoformat()
message = (
f&quot;ALERTA DE ESTOQUE BAIXO - &quot;
f&quot;Produto: {alert.product_name} (SKU: {alert.sku}) - &quot;
f&quot;Quantidade atual: {alert.current_quantity} - &quot;
f&quot;Mínimo requerido: {alert.min_quantity} - &quot;
f&quot;Horário: {alert.timestamp}&quot;
)
# Simulação de envio de notificação
logger.info(f&quot;Enviando alerta: {message}&quot;)
# Aqui poderia integrar com email, Slack, SMS, etc.
print(f&quot;[NOTIFICATION] {message}&quot;)
return {
&quot;status&quot;: &quot;success&quot;,
&quot;message&quot;: &quot;Alerta enviado com sucesso&quot;,
&quot;data&quot;: alert.dict()
}
except Exception as e:
logger.error(f&quot;Erro ao processar alerta: {str(e)}&quot;)
raise HTTPException(status_code=500, detail=&quot;Erro interno do servidor&quot;)
if __name__ == &quot;__main__&quot;:
import uvicorn
uvicorn.run(app, host=&quot;0.0.0.0&quot;, port=8000)