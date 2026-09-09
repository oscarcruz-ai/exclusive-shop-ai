import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


class EventReplayStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path,
            timeout=5,
        )
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_plugin_events (
                    tenant_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    processed_at TEXT NOT NULL,
                    PRIMARY KEY (tenant_id, event_id)
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_processed_plugin_events_date
                ON processed_plugin_events (processed_at)
                """
            )

    def claim(
        self,
        tenant_id: str,
        event_id: str,
    ) -> bool:
        """
        Registra un evento una sola vez.

        Devuelve:
        - True: el event_id es nuevo y queda reservado.
        - False: ya había sido procesado/reservado anteriormente.
        """
        tenant_id = str(tenant_id or "").strip()
        event_id = str(event_id or "").strip()

        if not tenant_id or not event_id:
            return False

        now = datetime.now(timezone.utc).isoformat()

        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO processed_plugin_events (
                        tenant_id,
                        event_id,
                        processed_at
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        tenant_id,
                        event_id,
                        now,
                    ),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def release(self, tenant_id: str, event_id: str) -> None:
        """Libera una reserva si el procesamiento del evento falla."""
        tenant_id = str(tenant_id or "").strip()
        event_id = str(event_id or "").strip()

        if not tenant_id or not event_id:
            return

        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM processed_plugin_events
                WHERE tenant_id = ? AND event_id = ?
                """,
                (tenant_id, event_id),
            )

    def cleanup(self, days: int = 7) -> None:
        """Elimina IDs antiguos para evitar crecimiento indefinido."""
        cutoff = (
            datetime.now(timezone.utc)
            - timedelta(days=days)
        ).isoformat()

        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM processed_plugin_events
                WHERE processed_at < ?
                """,
                (cutoff,),
            )
