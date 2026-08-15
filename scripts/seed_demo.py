from pathlib import Path
from app.analytics.analytics_store import AnalyticsStore
from app.analytics.attribution_store import AttributionStore

BASE=Path(__file__).resolve().parents[1]/"data"
BASE.mkdir(exist_ok=True)
analytics=AnalyticsStore(BASE/"shopagent_analytics.sqlite3")
attrs=AttributionStore(BASE/"shopagent_attribution.sqlite3")
tenant="demo-lumeauren"
for i in range(1284): analytics.record(tenant,"conversation",session_id=f"s{i}")
for i in range(347): analytics.record(tenant,"recommendation",session_id=f"s{i%1284}")
for i in range(86): analytics.record(tenant,"checkout_intent",session_id=f"s{i}",channel="web")
for i in range(31):
    sid=f"s{i}"
    attrs.register_checkout(tenant,sid,f"checkout-{i}")
    value=round(4850/31,2)
    attrs.mark_purchase(tenant,sid,str(1000+i),str(1000+i),value,"PEN","completed")
    analytics.record(tenant,"purchase",session_id=sid,channel="web",order_id=str(1000+i),value=value,currency="PEN")
print("Demo seeded for tenant:",tenant)
