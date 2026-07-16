from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.sales_agent import SalesAgent

app = FastAPI(
    title="Exclusive Shop AI",
    description="API del asistente inteligente de Exclusive Shop",
    version="1.0.0",
)

bot = SalesAgent()


class QuestionRequest(BaseModel):
    question: str


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
