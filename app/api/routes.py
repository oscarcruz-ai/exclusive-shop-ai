from fastapi import APIRouter

from app.chatbot import ExclusiveShopBot
from app.api.schemas import (
    QuestionRequest,
    AnswerResponse,
)

router = APIRouter()

bot = ExclusiveShopBot()


@router.get("/")
def home():
    return {
        "message": "Exclusive Shop AI API",
        "docs": "/docs"
    }


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(request: QuestionRequest):

    respuesta = bot.responder(
        pregunta=request.question
    )

    return AnswerResponse(
        answer=respuesta
    )