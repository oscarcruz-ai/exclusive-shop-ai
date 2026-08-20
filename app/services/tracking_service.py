from __future__ import annotations

from typing import Any, Dict, Optional

from app.services.woocommerce_service import WooCommerceService


class TrackingService:
    """Obtiene el seguimiento registrado en WooCommerce.

    Las transportistas se consultan automáticamente únicamente cuando exista
    una integración oficial, documentada y configurada. No se extrae ni se
    interpreta contenido de sus páginas públicas.
    """

    SHALOM_URL = "https://shalom.com.pe/rastrea/"
    OLVA_URL = "https://www.olvacourier.com/"

    def consultar_pedido(
        self,
        order_id: int,
        woocommerce: Optional[WooCommerceService] = None,
    ) -> Dict[str, Any]:
        """Consulta el seguimiento almacenado para un pedido de WooCommerce.

        ``woocommerce`` permite inyectar un cliente simulado en pruebas y evita
        crear una conexión/configuración nueva cuando el llamador ya la tiene.
        """
        try:
            servicio = woocommerce or WooCommerceService()
            seguimiento = servicio.obtener_seguimiento(order_id)
        except Exception:
            # No se expone información de configuración ni credenciales al
            # cliente. El detalle queda disponible en los registros del host.
            return {
                "ok": False,
                "order_id": order_id,
                "estado": None,
                "mensaje": (
                    "No se pudo recuperar el seguimiento del pedido en este "
                    "momento. Intenta nuevamente más tarde."
                ),
            }

        return self._resultado_pedido(order_id, seguimiento)

    def consultar_pedido_autorizado(
        self,
        order_id: int,
        email: str,
        woocommerce: Optional[WooCommerceService] = None,
    ) -> Dict[str, Any]:
        """Consulta el seguimiento solo si el correo coincide con el pedido.

        Se devuelve el mismo mensaje para un pedido inexistente o un correo que
        no coincide, para no revelar qué números de pedido son válidos.
        """
        try:
            servicio = woocommerce or WooCommerceService()
            pedido = servicio.obtener_pedido(order_id)
        except Exception:
            return {
                "ok": False,
                "order_id": order_id,
                "estado": None,
                "mensaje": (
                    "No se pudo recuperar el seguimiento del pedido en este "
                    "momento. Intenta nuevamente más tarde."
                ),
            }

        correo_pedido = (
            pedido.get("billing", {}).get("email", "")
            if pedido else ""
        )

        if self._normalizar_email(email) != self._normalizar_email(correo_pedido):
            return {
                "ok": False,
                "order_id": order_id,
                "estado": None,
                "mensaje": (
                    "No encontramos un pedido asociado a esos datos. "
                    "Verifica el número de pedido y el correo de compra."
                ),
            }

        return self._resultado_pedido(
            order_id,
            WooCommerceService.extraer_seguimiento(pedido),
        )

    @staticmethod
    def _normalizar_email(email: str) -> str:
        return (email or "").strip().casefold()

    def _resultado_pedido(self, order_id: int, seguimiento: Optional[Dict[str, Any]]):
        if not seguimiento:
            return {
                "ok": False,
                "order_id": order_id,
                "empresa": None,
                "codigo": None,
                "numero_orden": None,
                "estado": None,
                "mensaje": "El pedido no tiene información de seguimiento registrada.",
            }

        resultado = self.consultar(
            empresa=seguimiento.get("empresa"),
            codigo=seguimiento.get("codigo"),
            numero_orden=seguimiento.get("numero_orden"),
        )
        resultado["order_id"] = order_id
        return resultado

    def consultar(self, empresa, codigo, numero_orden=None):

        empresa = (empresa or "").strip().lower()
        codigo = (codigo or "").strip()

        if not codigo:
            return {
                "ok": False,
                "empresa": empresa,
                "codigo": None,
                "estado": None,
                "mensaje": "No hay código de seguimiento registrado."
            }

        if empresa == "shalom":
            return self._consultar_shalom(
                codigo=codigo,
                numero_orden=numero_orden
            )

        if empresa in ("olva", "olva courier"):
            return self._consultar_olva(codigo)

        return {
            "ok": False,
            "empresa": empresa,
            "codigo": codigo,
            "estado": None,
            "mensaje": f"No tengo integración de tracking para {empresa or 'esta empresa'}."
        }

    # ==========================================================
    # SHALOM
    # ==========================================================

    def _consultar_shalom(self, codigo, numero_orden=None):

        resultado = {
            "ok": False,
            "empresa": "Shalom",
            "codigo": codigo,
            "numero_orden": numero_orden,
            "estado": None,
            "detalle": None,
            "url": self.SHALOM_URL,
            "fuente": "registro_woocommerce",
            "consulta_automatica": False,
        }

        # Shalom requiere número de orden y código
        # para realizar el rastreo.
        if not numero_orden:
            resultado["mensaje"] = (
                "El envío de Shalom requiere también el número "
                "de orden para consultar el rastreo."
            )
            return resultado

        resultado["mensaje"] = (
            "El envío está registrado. Consulta el estado en el portal oficial "
            "de Shalom con el número de orden y el código de seguimiento."
        )

        return resultado

    # ==========================================================
    # OLVA
    # ==========================================================

    def _consultar_olva(self, codigo):

        resultado = {
            "ok": False,
            "empresa": "Olva Courier",
            "codigo": codigo,
            "estado": None,
            "detalle": None,
            "url": self.OLVA_URL,
            "fuente": "registro_woocommerce",
            "consulta_automatica": False,
        }

        resultado["mensaje"] = (
            "El código de Olva está registrado. Consulta el estado en el portal "
            "oficial de Olva con el número de tracking."
        )

        return resultado
