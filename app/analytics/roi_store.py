from __future__ import annotations
from .analytics_store import AnalyticsStore

class ROIStore:
    def __init__(self, analytics: AnalyticsStore):
        self.analytics=analytics

    def dashboard(self, tenant_id:str, days:int=30, monthly_fee:float=0, currency="PEN"):
        s=self.analytics.summary(tenant_id,days)
        revenue=s["revenue"]
        fee=float(monthly_fee or 0)
        return {
            **s,
            "currency": currency,
            "monthly_fee": fee,
            "roi_multiple": round(revenue/fee,2) if fee>0 else None,
            "roas_percent": round((revenue/fee)*100,2) if fee>0 else None,
            "revenue_per_conversation": round(revenue/s["conversations"],2) if s["conversations"] else 0,
            "average_order_value": round(revenue/s["purchases"],2) if s["purchases"] else 0,
        }
