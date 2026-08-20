from __future__ import annotations

import os

import truststore

# Requests suele usar el paquete certifi. Usar el almacén de confianza de
# Windows conserva la validación TLS e incluye las cadenas que el sistema ya
# reconoce.
truststore.inject_into_ssl()

import requests
from dotenv import load_dotenv


class WooCommerceService:

    def __init__(self):
        load_dotenv()

        self.base_url = os.getenv(
            "WOOCOMMERCE_URL"
        ).rstrip("/")

        self.consumer_key = os.getenv(
            "WOOCOMMERCE_CONSUMER_KEY"
        )

        self.consumer_secret = os.getenv(
            "WOOCOMMERCE_CONSUMER_SECRET"
        )

        if not self.base_url:
            raise ValueError(
                "Falta WOOCOMMERCE_URL en .env"
            )

        if not self.consumer_key:
            raise ValueError(
                "Falta WOOCOMMERCE_CONSUMER_KEY en .env"
            )

        if not self.consumer_secret:
            raise ValueError(
                "Falta WOOCOMMERCE_CONSUMER_SECRET en .env"
            )

    def _get(self, endpoint, params=None):
        url = (
            f"{self.base_url}"
            f"/wp-json/wc/v3/{endpoint}"
        )

        response = requests.get(
            url,
            auth=(
                self.consumer_key,
                self.consumer_secret,
            ),
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def obtener_productos(
        self,
        page=1,
        per_page=10,
    ):
        return self._get(
            "products",
            params={
                "page": page,
                "per_page": per_page,
            },
        )

    def obtener_producto(
        self,
        product_id,
    ):
        return self._get(
            f"products/{product_id}"
        )

    def obtener_pedidos(
        self,
        page=1,
        per_page=10,
    ):
        return self._get(
            "orders",
            params={
                "page": page,
                "per_page": per_page,
            },
        )

    def obtener_pedido(
        self,
        order_id,
    ):
        return self._get(
            f"orders/{order_id}"
        )

    def obtener_pedido(
        self,
        order_id,
    ):
        return self._get(
            f"orders/{order_id}"
        )

    def actualizar_meta_pedido(self, order_id, key, value):
        url = (
            f"{self.base_url}"
            f"/wp-json/wc/v3/orders/{order_id}"
        )

        response = requests.put(
            url,
            auth=(
                self.consumer_key,
                self.consumer_secret
            ),
            json={
                "meta_data": [
                    {
                        "key": key,
                        "value": value
                    }
                ]
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def eliminar_meta_pedido(self, order_id, key):
        pedido = self.obtener_pedido(order_id)

        if not pedido:
            return None

        meta_data = pedido.get("meta_data", [])

        meta_data_filtrada = [
            meta
            for meta in meta_data
            if meta.get("key") != key
        ]

        url = (
            f"{self.base_url}"
            f"/wp-json/wc/v3/orders/{order_id}"
        )

        response = requests.put(
            url,
            auth=(
                self.consumer_key,
                self.consumer_secret
            ),
            json={
                "meta_data": meta_data_filtrada
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def guardar_seguimiento(
        self,
        order_id,
        empresa,
        codigo,
        numero_orden=None
    ):
        self.actualizar_meta_pedido(
            order_id,
            "_empresa_envio",
            empresa
        )

        self.actualizar_meta_pedido(
            order_id,
            "_codigo_seguimiento",
            codigo
        )

        if numero_orden:
            return self.actualizar_meta_pedido(
                order_id,
                "_numero_orden_envio",
                numero_orden
            )

        return self.obtener_pedido(order_id)

    @staticmethod
    def extraer_seguimiento(pedido):
        """Extrae los metadatos de seguimiento de un pedido ya obtenido."""
        if not pedido:
            return None

        seguimiento = {
            "empresa": None,
            "codigo": None,
            "numero_orden": None
        }

        for meta in pedido.get("meta_data", []):
            key = meta.get("key")
            value = meta.get("value")

            if key == "_empresa_envio":
                seguimiento["empresa"] = value

            elif key == "_codigo_seguimiento":
                seguimiento["codigo"] = value

            elif key == "_numero_orden_envio":
                seguimiento["numero_orden"] = value

        if not any(seguimiento.values()):
            return None

        return seguimiento

    def obtener_seguimiento(self, order_id):
        return self.extraer_seguimiento(
            self.obtener_pedido(order_id)
        )
