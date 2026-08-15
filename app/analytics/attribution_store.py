from __future__ import annotations
import sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

class AttributionStore:
    def __init__(self, db_path:str|Path):
        self.db_path=str(db_path); Path(self.db_path).parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(self.db_path) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS attributions(
                id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, session_id TEXT NOT NULL,
                channel TEXT NOT NULL, checkout_id TEXT, order_id TEXT UNIQUE,
                order_number TEXT, status TEXT NOT NULL, value REAL, currency TEXT,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
            c.execute("CREATE INDEX IF NOT EXISTS idx_attr_tenant ON attributions(tenant_id,created_at)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_attr_session ON attributions(tenant_id,session_id)")

    def register_checkout(self,tenant_id,session_id,checkout_id,channel="web"):
        now=datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as c:
            c.execute("""INSERT INTO attributions
                (id,tenant_id,session_id,channel,checkout_id,status,created_at,updated_at)
                VALUES(?,?,?,?,?,?,?,?)""",
                (str(uuid.uuid4()),tenant_id,session_id,channel,checkout_id,"checkout_intent",now,now))

    def find_session_for_order(self,tenant_id,order_id,order_meta=None):
        if order_meta:
            for key in ("shopagent_session_id","_shopagent_session_id","shopagent_checkout_id","_shopagent_checkout"):
                for item in order_meta:
                    if item.get("key")==key and item.get("value"):
                        val=str(item["value"])
                        with sqlite3.connect(self.db_path) as c:
                            row=c.execute("""SELECT session_id FROM attributions
                                WHERE tenant_id=? AND (session_id=? OR checkout_id=?) ORDER BY created_at DESC LIMIT 1""",
                                (tenant_id,val,val)).fetchone()
                        if row: return row[0]
        with sqlite3.connect(self.db_path) as c:
            row=c.execute("""SELECT session_id FROM attributions WHERE tenant_id=?
                AND order_id IS NULL ORDER BY created_at DESC LIMIT 1""",(tenant_id,)).fetchone()
        return row[0] if row else None

    def mark_purchase(self,tenant_id,session_id,order_id,order_number,value,currency,status):
        now=datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as c:
            c.execute("""INSERT INTO attributions
                (id,tenant_id,session_id,channel,order_id,order_number,status,value,currency,created_at,updated_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(order_id) DO UPDATE SET status=excluded.status,value=excluded.value,
                currency=excluded.currency,order_number=excluded.order_number,updated_at=excluded.updated_at""",
                (str(uuid.uuid4()),tenant_id,session_id,"web",str(order_id),str(order_number),
                 status,float(value or 0),currency,now,now))

    def get(self,tenant_id,order_id):
        with sqlite3.connect(self.db_path) as c:
            r=c.execute("SELECT * FROM attributions WHERE tenant_id=? AND order_id=?",(tenant_id,str(order_id))).fetchone()
        return dict(r) if r else None
