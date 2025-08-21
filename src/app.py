from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service", version="1.0.0")


class AlertRequest(BaseModel):
    product_name: str
    current_quantity: int
    min_quantity: int
    sku: str
    timestamp: str = None


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/alert")
async def send_alert(alert: AlertRequest):
    """Endpoint para enviar alertas de estoque baixo"""
    try:
        if not alert.timestamp:
            alert.timestamp = datetime.utcnow().isoformat()
        
        message = (
            f"ALERTA DE ESTOQUE BAIXO - "
            f"Produto: {alert.product_name} (SKU: {alert.sku}) - "
            f"Quantidade atual: {alert.current_quantity} - "
            f"Mínimo requerido: {alert.min_quantity} - "
            f"Horário: {alert.timestamp}"
        )
        
        # Simulação de envio de notificação
        logger.info(f"Enviando alerta: {message}")
        
        # Aqui poderia integrar com email, Slack, SMS, etc.
        print(f"[NOTIFICATION] {message}")
        
        return {
            "status": "success",
            "message": "Alerta enviado com sucesso",
            "data": alert.dict()
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar alerta: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
