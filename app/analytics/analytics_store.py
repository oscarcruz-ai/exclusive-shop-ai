from __future__ import annotations
import sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

class AnalyticsStore:
    def __init__(self, db_path: str|Path):
        self.db_path=str(db_path)
        Path(self.db_path).parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(self.db_path) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS events(
                id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, session_id TEXT,
                channel TEXT NOT NULL, event_type TEXT NOT NULL, product_id TEXT,
                variation_id TEXT, order_id TEXT, value REAL, currency TEXT,
                metadata TEXT, created_at TEXT NOT NULL)""")
            c.execute("CREATE INDEX IF NOT EXISTS idx_events_tenant_time ON events(tenant_id,created_at)")
            c.execute("CREATE INDEX IF NOT EXISTS idx_events_tenant_type ON events(tenant_id,event_type)")

    def record(self, tenant_id, event_type, *, session_id=None, channel="web",
               product_id=None, variation_id=None, order_id=None,
               value=None, currency=None, metadata="{}"):
        now=datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as c:
            c.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                      (str(uuid.uuid4()),tenant_id,session_id,channel,event_type,
                       str(product_id) if product_id is not None else None,
                       str(variation_id) if variation_id is not None else None,
                       str(order_id) if order_id is not None else None,
                       value,currency,metadata,now))
        return now

    def summary(self, tenant_id, days=30):
        with sqlite3.connect(self.db_path) as c:
            rows=c.execute("""SELECT event_type, COUNT(*) FROM events
                              WHERE tenant_id=? AND created_at >= datetime('now', ?)
                              GROUP BY event_type""",(tenant_id,f"-{int(days)} days")).fetchall()
        counts={k:int(v) for k,v in rows}
        conversations=counts.get("conversation",0)
        purchases=counts.get("purchase",0)
        checkouts=counts.get("checkout_intent",0)
        revenue=self.revenue(tenant_id,days)
        return {
            "days":days,"conversations":conversations,
            "product_views":counts.get("product_view",0),
            "recommendations":counts.get("recommendation",0),
            "checkout_intents":checkouts,"purchases":purchases,
            "revenue":round(revenue,2),
            "checkout_rate":round(checkouts/conversations*100,2) if conversations else 0,
            "purchase_rate":round(purchases/conversations*100,2) if conversations else 0,
            "checkout_to_purchase_rate":round(purchases/checkouts*100,2) if checkouts else 0
        }

    def revenue(self, tenant_id, days=30):
        with sqlite3.connect(self.db_path) as c:
            r=c.execute("""SELECT COALESCE(SUM(value),0) FROM events
                           WHERE tenant_id=? AND event_type='purchase'
                           AND created_at >= datetime('now', ?)""",
                        (tenant_id,f"-{int(days)} days")).fetchone()
        return float(r[0] or 0)

    def daily(self, tenant_id, days=14):
        with sqlite3.connect(self.db_path) as c:
            rows=c.execute("""SELECT substr(created_at,1,10) day,event_type,COUNT(*)
                              FROM events WHERE tenant_id=? AND created_at >= datetime('now', ?)
                              GROUP BY day,event_type ORDER BY day""",
                           (tenant_id,f"-{int(days)} days")).fetchall()
        out={}
        for day,typ,count in rows:
            out.setdefault(day,{})[typ]=count
        return out
