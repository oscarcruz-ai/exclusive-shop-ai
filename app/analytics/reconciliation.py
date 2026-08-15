from __future__ import annotations
import sqlite3
from pathlib import Path

class Reconciliation:
    def __init__(self, db_path:str|Path):
        self.db_path=str(db_path)

    def summary(self,tenant_id:str,days:int=30):
        with sqlite3.connect(self.db_path) as c:
            rows=c.execute("""SELECT status,COALESCE(SUM(value),0),COUNT(*) FROM attributions
                WHERE tenant_id=? AND created_at >= datetime('now', ?)
                GROUP BY status""",(tenant_id,f"-{int(days)} days")).fetchall()
        gross=paid=refunded=0.0
        counts={}
        for status,value,count in rows:
            counts[status]=int(count)
            if status in ("processing","completed"): paid+=float(value)
            if status=="refunded": refunded+=float(value)
            gross+=float(value)
        return {"gross_attributed":round(gross,2),"paid_attributed":round(paid,2),
                "refunded_attributed":round(refunded,2),
                "net_attributed":round(paid-refunded,2),"orders_by_status":counts}
