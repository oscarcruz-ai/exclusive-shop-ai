from fastapi import FastAPI
from app.agents.sales_agent import SalesAgent
from app.api.schemas import QuestionRequest, TrackingRequest
from app.services.tracking_service import TrackingService

app = FastAPI(
    title="Exclusive Shop AI",
    description="API del asistente inteligente de Exclusive Shop",
    version="1.0.0",
)

bot = SalesAgent()


@app.get("/")
def home():
    return {
        "message": "Exclusive Shop AI API",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    respuesta = bot.responder(
        pregunta=request.question
    )

    return {
        "answer": respuesta
    }


@app.post("/tracking")
def tracking(request: TrackingRequest):
    """Devuelve seguimiento únicamente tras comprobar el correo de compra."""
    return TrackingService().consultar_pedido_autorizado(
        order_id=request.order_id,
        email=request.email,
    )
