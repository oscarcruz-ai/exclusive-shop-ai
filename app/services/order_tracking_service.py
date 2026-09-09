import re
from pathlib import Path

from app.integrations.order_store import OrderStore


class OrderTrackingService:
    EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
    ORDER_RE = re.compile(r"(?:pedido|orden)\s*(?:n[.°ºo]*\s*)?#?\s*(\d{4,})", re.IGNORECASE)

    TRACKING_KEYWORDS = (
        "donde esta mi pedido",
        "dónde está mi pedido",
        "estado de mi pedido",
        "estado del pedido",
        "seguir mi pedido",
        "seguimiento de mi pedido",
        "rastrear mi pedido",
        "tracking de mi pedido",
        "consultar mi pedido",
        "consultar mi pedida",
        "ver mi pedido",
        "ver mi pedida",
        "mi pedido",
        "mi pedida",
    )

    STATUS_LABELS = {
        "pending": "Pendiente de pago",
        "processing": "En procesamiento",
        "on-hold": "En espera",
        "completed": "Completado",
        "cancelled": "Cancelado",
        "refunded": "Reembolsado",
        "failed": "Fallido",
    }

    def __init__(
        self,
        tenant_id: str = "exclusive-shop",
        db_path: Path = Path("data/shopagent_orders.sqlite3"),
    ):
        self.tenant_id = tenant_id
        self.orders = OrderStore(db_path)
        self.pending_order_number: str | None = None
        self.awaiting_order_number: bool = False

    def responder(self, pregunta: str) -> str | None:
        texto = pregunta.strip()
        texto_lower = texto.lower()
        email = self._extract_email(texto)
        order_number = self._extract_order_number(texto)
        is_tracking_query = self._is_tracking_query(texto_lower)

        # Si ya pedimos el correo, esperamos un correo válido.
        if self.pending_order_number and email:
            order_number = self.pending_order_number
            return self._lookup_and_format(order_number, email)

        # Si antes pedimos el número de pedido, aceptamos un número solo.
        if self.awaiting_order_number:
            standalone = re.fullmatch(r"\s*#?(\d{4,})\s*", texto)

            if standalone:
                order_number = standalone.group(1)
                self.awaiting_order_number = False
                self.pending_order_number = order_number

                return (
                    f"Encontré el número de pedido *{order_number}*. Para proteger "
                    "la información de tu compra, indícame el correo electrónico "
                    "que utilizaste al realizar el pedido."
                )

        if not is_tracking_query:
            return None

        if not order_number:
            self.awaiting_order_number = True

            return (
                "Claro. Para consultar el estado de tu compra, indícame el "
                "número de pedido que aparece en tu confirmación de compra."
            )

        if not email:
            self.awaiting_order_number = False
            self.pending_order_number = order_number

            return (
                f"Encontré el número de pedido *{order_number}*. Para proteger "
                "la información de tu compra, indícame el correo electrónico "
                "que utilizaste al realizar el pedido."
            )

        return self._lookup_and_format(order_number, email)

    def _lookup_and_format(self, order_number: str, email: str) -> str:
        order = self.orders.lookup_customer_order(
            tenant_id=self.tenant_id,
            order_number=order_number,
            email=email,
        )
        self.pending_order_number = None
        self.awaiting_order_number = False

        if not order:
            return (
                "No pude verificar un pedido con ese número y correo. Revisa "
                "que ambos datos sean los mismos que utilizaste en la compra. "
                "Por seguridad no puedo mostrar información si no coinciden."
            )

        status_raw = str(order.get("status") or "").strip().lower()
        status = self.STATUS_LABELS.get(status_raw, status_raw.replace("-", " ").title())
        carrier = str(order.get("tracking_carrier") or "").strip()
        tracking_code = str(order.get("tracking_code") or "").strip()
        carrier_order_number = str(order.get("tracking_order_number") or "").strip()

        # WooCommerce puede mantener el pedido en "on-hold" incluso después
        # de registrar el envío. Si ya existe transportista + tracking,
        # mostramos al cliente el estado logístico más útil sin alterar el
        # estado original guardado en WooCommerce.
        has_shipping_tracking = bool(carrier and tracking_code)

        lines = [f"✅ **Pedido {order_number} verificado**"]

        if has_shipping_tracking:
            lines.append("📦 **Tu pedido ya fue enviado y tiene seguimiento disponible.**")
        else:
            lines.append(f"**Estado:** {status or 'Sin estado disponible'}")

        if carrier:
            lines.append(f"**Transportista:** {carrier}")

        if tracking_code:
            lines.append(f"**Código de seguimiento:** {tracking_code}")

        if carrier_order_number:
            lines.append(f"**N.º de orden del transportista:** {carrier_order_number}")

        if carrier.lower() == "shalom" and tracking_code and carrier_order_number:
            lines.append(
                "[🚚 **Rastrear mi pedido en Shalom**](https://shalom.com.pe/rastrea/)"
            )
            lines.append(
                "En Shalom necesitarás el **N.º de orden del transportista** y el "
                "**código de seguimiento** mostrados arriba."
            )
        elif carrier.lower().startswith("olva") and tracking_code:
            lines.append(
                "[🚚 **Rastrear mi pedido en Olva Courier**](https://www.olvacourier.com/)"
            )
        elif not tracking_code:
            lines.append(
                "Aún no tengo un código de seguimiento registrado para este pedido."
            )

        return "\n\n".join(lines)

    @classmethod
    def _extract_email(cls, text: str) -> str | None:
        match = cls.EMAIL_RE.search(text)
        return match.group(0).lower() if match else None

    @classmethod
    def _extract_order_number(cls, text: str) -> str | None:
        match = cls.ORDER_RE.search(text)
        if match:
            return match.group(1)

        # Permite frases naturales como "¿dónde está mi pedido? 42916".
        if cls._is_tracking_query(text.lower()):
            standalone = re.search(r"\b(\d{4,})\b", text)
            if standalone:
                return standalone.group(1)

        return None

    @classmethod
    def _is_tracking_query(cls, text_lower: str) -> bool:
        return any(keyword in text_lower for keyword in cls.TRACKING_KEYWORDS)
