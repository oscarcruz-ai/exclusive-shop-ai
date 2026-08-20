import unittest

from app.services.tracking_service import TrackingService


class WooCommerceConSeguimiento:
    def obtener_seguimiento(self, order_id):
        assert order_id == 42818
        return {
            "empresa": "Shalom",
            "codigo": "TEST-SHALOM-001",
            "numero_orden": "TEST-ORDEN-001",
        }


class WooCommerceSinSeguimiento:
    def obtener_seguimiento(self, order_id):
        return None


class WooCommercePedidoAutorizado:
    def obtener_pedido(self, order_id):
        assert order_id == 42818
        return {
            "billing": {"email": "cliente@ejemplo.com"},
            "meta_data": [
                {"key": "_empresa_envio", "value": "Olva Courier"},
                {"key": "_codigo_seguimiento", "value": "26-12345678"},
            ],
        }


class TrackingServiceTests(unittest.TestCase):
    def test_consultar_pedido_recupera_datos_de_woocommerce_sin_inventar_estado(self):
        resultado = TrackingService().consultar_pedido(
            42818,
            woocommerce=WooCommerceConSeguimiento(),
        )

        self.assertEqual(resultado["order_id"], 42818)
        self.assertEqual(resultado["empresa"], "Shalom")
        self.assertEqual(resultado["codigo"], "TEST-SHALOM-001")
        self.assertEqual(resultado["numero_orden"], "TEST-ORDEN-001")
        self.assertIsNone(resultado["estado"])
        self.assertFalse(resultado["consulta_automatica"])
        self.assertEqual(resultado["url"], TrackingService.SHALOM_URL)

    def test_consultar_pedido_informa_cuando_no_hay_tracking(self):
        resultado = TrackingService().consultar_pedido(
            1,
            woocommerce=WooCommerceSinSeguimiento(),
        )

        self.assertFalse(resultado["ok"])
        self.assertIsNone(resultado["estado"])
        self.assertIn("no tiene información", resultado["mensaje"])

    def test_olva_conserva_el_codigo_y_dirige_al_portal_oficial(self):
        resultado = TrackingService().consultar("Olva Courier", "26-12345678")

        self.assertEqual(resultado["empresa"], "Olva Courier")
        self.assertEqual(resultado["codigo"], "26-12345678")
        self.assertIsNone(resultado["estado"])
        self.assertFalse(resultado["consulta_automatica"])
        self.assertEqual(resultado["url"], TrackingService.OLVA_URL)

    def test_consultar_pedido_autorizado_requiere_el_correo_de_compra(self):
        resultado = TrackingService().consultar_pedido_autorizado(
            42818,
            "CLIENTE@EJEMPLO.COM",
            woocommerce=WooCommercePedidoAutorizado(),
        )

        self.assertEqual(resultado["empresa"], "Olva Courier")
        self.assertEqual(resultado["codigo"], "26-12345678")

    def test_consultar_pedido_autorizado_no_revela_datos_con_correo_incorrecto(self):
        resultado = TrackingService().consultar_pedido_autorizado(
            42818,
            "otra-persona@ejemplo.com",
            woocommerce=WooCommercePedidoAutorizado(),
        )

        self.assertFalse(resultado["ok"])
        self.assertNotIn("empresa", resultado)
        self.assertIn("No encontramos", resultado["mensaje"])
