import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from app.agents.sales_agent import SalesAgent
from app.analytics.analytics_store import AnalyticsStore
from app.integrations.order_store import OrderStore

app = FastAPI(
    title="Exclusive Shop AI",
    description="API del asistente inteligente de Exclusive Shop",
    version="1.3.0",
)

bot = SalesAgent()
analytics = AnalyticsStore(Path("data/shopagent_events.sqlite3"))
orders = OrderStore(Path("data/shopagent_orders.sqlite3"))

SIGNATURE_MAX_AGE_SECONDS = 300


class QuestionRequest(BaseModel):
    question: str


class IntegrationEventRequest(BaseModel):
    event: str
    event_id: str | None = None
    tenant_id: str
    occurred_at: str | None = None
    source: str = "woocommerce"
    store_url: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


def _plugin_secret() -> str:
    expected = os.getenv("SHOPAGENT_PLUGIN_API_KEY", "").strip()
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="La autenticación del plugin no está configurada en el servidor.",
        )
    return expected


def _verify_plugin_api_key(authorization: str | None, expected: str) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Autenticación del plugin inválida.")

    received = authorization.removeprefix("Bearer ").strip()
    if not secrets.compare_digest(received, expected):
        raise HTTPException(status_code=401, detail="Autenticación del plugin inválida.")


def _verify_plugin_signature(
    *,
    raw_body: bytes,
    expected_secret: str,
    timestamp: str | None,
    event_id: str | None,
    signature: str | None,
    body_event_id: str | None,
) -> None:
    """Valida integridad y frescura del evento enviado por WordPress."""
    if not timestamp or not event_id or not signature:
        raise HTTPException(status_code=401, detail="Firma del evento inválida.")

    if body_event_id and not secrets.compare_digest(body_event_id, event_id):
        raise HTTPException(status_code=401, detail="Firma del evento inválida.")

    try:
        event_timestamp = int(timestamp)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Firma del evento inválida.")

    if abs(int(time.time()) - event_timestamp) > SIGNATURE_MAX_AGE_SECONDS:
        raise HTTPException(status_code=401, detail="El evento ha expirado.")

    signed_payload = (
        timestamp.encode("utf-8")
        + b"."
        + event_id.encode("utf-8")
        + b"."
        + raw_body
    )
    digest = hmac.new(
        expected_secret.encode("utf-8"),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()
    expected_signature = f"sha256={digest}"

    if not secrets.compare_digest(signature.strip(), expected_signature):
        raise HTTPException(status_code=401, detail="Firma del evento inválida.")


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
async def receive_integration_event(
    request: Request,
    authorization: str | None = Header(default=None),
    x_shopagent_timestamp: str | None = Header(default=None),
    x_shopagent_event_id: str | None = Header(default=None),
    x_shopagent_signature: str | None = Header(default=None),
):
    expected_secret = _plugin_secret()
    _verify_plugin_api_key(authorization, expected_secret)

    raw_body = await request.body()
    try:
        parsed = IntegrationEventRequest.model_validate_json(raw_body)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Evento inválido.") from exc

    _verify_plugin_signature(
        raw_body=raw_body,
        expected_secret=expected_secret,
        timestamp=x_shopagent_timestamp,
        event_id=x_shopagent_event_id,
        signature=x_shopagent_signature,
        body_event_id=parsed.event_id,
    )

    allowed_events = {
        "integration.test",
        "order.created",
        "order.updated",
    }

    if parsed.event not in allowed_events:
        raise HTTPException(
            status_code=422,
            detail=f"Evento no soportado: {parsed.event}",
        )

    order_id = parsed.data.get("order_id")
    value = parsed.data.get("total")
    currency = parsed.data.get("currency")

    try:
        numeric_value = float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        numeric_value = None

    metadata = {
        "event_id": parsed.event_id,
        "source": parsed.source,
        "store_url": parsed.store_url,
        "occurred_at": parsed.occurred_at,
        "payload": parsed.data,
    }

    recorded_at = analytics.record(
        tenant_id=parsed.tenant_id,
        event_type=parsed.event,
        channel="woocommerce",
        order_id=order_id,
        value=numeric_value,
        currency=currency,
        metadata=json.dumps(metadata, ensure_ascii=False, default=str),
    )

    order_synced_at = None
    if parsed.event in {"order.created", "order.updated"}:
        try:
            order_synced_at = orders.upsert(parsed.tenant_id, parsed.data)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "ok": True,
        "event": parsed.event,
        "event_id": parsed.event_id,
        "tenant_id": parsed.tenant_id,
        "recorded_at": recorded_at,
        "order_synced_at": order_synced_at,
    }
