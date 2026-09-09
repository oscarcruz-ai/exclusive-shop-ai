import json
import os
import secrets
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from app.agents.sales_agent import SalesAgent
from app.analytics.analytics_store import AnalyticsStore
from app.integrations.order_store import OrderStore

app = FastAPI(
    title="Exclusive Shop AI",
    description="API del asistente inteligente de Exclusive Shop",
    version="1.2.0",
)

bot = SalesAgent()
analytics = AnalyticsStore(Path("data/shopagent_events.sqlite3"))
orders = OrderStore(Path("data/shopagent_orders.sqlite3"))


class QuestionRequest(BaseModel):
    question: str


class IntegrationEventRequest(BaseModel):
    event: str
    tenant_id: str
    occurred_at: str | None = None
    source: str = "woocommerce"
    store_url: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


def _verify_plugin_api_key(authorization: str | None) -> None:
    expected = os.getenv("SHOPAGENT_PLUGIN_API_KEY", "").strip()

    if not expected:
        raise HTTPException(
            status_code=503,
            detail="SHOPAGENT_PLUGIN_API_KEY no está configurada en el servidor.",
        )

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta Authorization Bearer token.")

    received = authorization.removeprefix("Bearer ").strip()
    if not secrets.compare_digest(received, expected):
        raise HTTPException(status_code=401, detail="API key inválida.")


@app.get("/")
def home():
    return {
        "message": "Exclusive Shop AI API",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    respuesta = bot.responder(
        pregunta=request.question,
    )

    return {
        "answer": respuesta,
    }


@app.post("/v1/events")
def receive_integration_event(
    request: IntegrationEventRequest,
    authorization: str | None = Header(default=None),
):
    _verify_plugin_api_key(authorization)

    allowed_events = {
        "integration.test",
        "order.created",
        "order.updated",
    }

    if request.event not in allowed_events:
        raise HTTPException(
            status_code=422,
            detail=f"Evento no soportado: {request.event}",
        )

    order_id = request.data.get("order_id")
    value = request.data.get("total")
    currency = request.data.get("currency")

    try:
        numeric_value = float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        numeric_value = None

    metadata = {
        "source": request.source,
        "store_url": request.store_url,
        "occurred_at": request.occurred_at,
        "payload": request.data,
    }

    recorded_at = analytics.record(
        tenant_id=request.tenant_id,
        event_type=request.event,
        channel="woocommerce",
        order_id=order_id,
        value=numeric_value,
        currency=currency,
        metadata=json.dumps(metadata, ensure_ascii=False, default=str),
    )

    order_synced_at = None
    if request.event in {"order.created", "order.updated"}:
        try:
            order_synced_at = orders.upsert(request.tenant_id, request.data)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "ok": True,
        "event": request.event,
        "tenant_id": request.tenant_id,
        "recorded_at": recorded_at,
        "order_synced_at": order_synced_at,
    }
