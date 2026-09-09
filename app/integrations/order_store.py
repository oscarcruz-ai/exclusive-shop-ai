import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class OrderStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS order_snapshots (
                    tenant_id TEXT NOT NULL,
                    order_id TEXT NOT NULL,
                    order_number TEXT,
                    status TEXT,
                    total REAL,
                    currency TEXT,
                    billing_email TEXT,
                    billing_phone TEXT,
                    tracking_carrier TEXT,
                    tracking_code TEXT,
                    tracking_order_number TEXT,
                    payload TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (tenant_id, order_id)
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_order_snapshots_lookup
                ON order_snapshots (tenant_id, order_number, billing_email)
                """
            )

    def upsert(self, tenant_id: str, payload: dict[str, Any]) -> str:
        order_id = str(payload.get("order_id") or "").strip()
        if not order_id:
            raise ValueError("order_id es obligatorio para guardar el pedido")

        billing = payload.get("billing") or {}
        tracking = payload.get("tracking") or {}
        updated_at = datetime.now(timezone.utc).isoformat()

        try:
            total = float(payload.get("total")) if payload.get("total") not in (None, "") else None
        except (TypeError, ValueError):
            total = None

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO order_snapshots (
                    tenant_id, order_id, order_number, status, total, currency,
                    billing_email, billing_phone, tracking_carrier, tracking_code,
                    tracking_order_number, payload, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(tenant_id, order_id) DO UPDATE SET
                    order_number = excluded.order_number,
                    status = excluded.status,
                    total = excluded.total,
                    currency = excluded.currency,
                    billing_email = excluded.billing_email,
                    billing_phone = excluded.billing_phone,
                    tracking_carrier = excluded.tracking_carrier,
                    tracking_code = excluded.tracking_code,
                    tracking_order_number = excluded.tracking_order_number,
                    payload = excluded.payload,
                    updated_at = excluded.updated_at
                """,
                (
                    tenant_id,
                    order_id,
                    str(payload.get("order_number") or ""),
                    str(payload.get("status") or ""),
                    total,
                    payload.get("currency"),
                    str(billing.get("email") or "").strip().lower(),
                    str(billing.get("phone") or "").strip(),
                    str(tracking.get("carrier") or "").strip(),
                    str(tracking.get("code") or "").strip(),
                    str(tracking.get("carrier_order_number") or "").strip(),
                    json.dumps(payload, ensure_ascii=False, default=str),
                    updated_at,
                ),
            )

        return updated_at

    def get_by_order_id(self, tenant_id: str, order_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM order_snapshots
                WHERE tenant_id = ? AND order_id = ?
                LIMIT 1
                """,
                (tenant_id, str(order_id)),
            ).fetchone()
        return self._row_to_dict(row)

    def lookup_customer_order(
        self,
        tenant_id: str,
        order_number: str,
        email: str,
    ) -> dict[str, Any] | None:
        normalized_email = email.strip().lower()
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM order_snapshots
                WHERE tenant_id = ?
                  AND order_number = ?
                  AND billing_email = ?
                LIMIT 1
                """,
                (tenant_id, str(order_number).strip(), normalized_email),
            ).fetchone()
        return self._row_to_dict(row)

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        result = dict(row)
        try:
            result["payload"] = json.loads(result.get("payload") or "{}")
        except json.JSONDecodeError:
            result["payload"] = {}
        return result
