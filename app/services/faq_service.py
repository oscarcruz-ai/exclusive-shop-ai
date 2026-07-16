from app.constants.faq_patterns import FAQ_PATTERNS
from app.services.brand_service import BrandService
from app.services.topic_detector import TopicDetector


class FAQService:

    def __init__(self):

        self.brand_service = BrandService()

        self.topic_detector = TopicDetector()

    def responder(self, pregunta):

        topics = self.topic_detector.detectar(
            pregunta
        )

        respuestas = []

        # =====================================
        # Tienda física
        # =====================================

        if "tienda" in topics:

            respuestas.append(
                "🏪 Actualmente somos una tienda 100% online.\n\n"
                "Todos nuestros pedidos se entregan directamente "
                "en el domicilio u oficina del cliente mediante "
                "servicio de envío."
            )

        # =====================================
        # Tiempo de entrega
        # =====================================

        if "tiempo_entrega" in topics:

            respuestas.append(
                "📦 Todos nuestros productos son importados bajo pedido.\n\n"
                "⏳ El tiempo estimado de entrega es de "
                "16 a 18 días hábiles.\n\n"
                "Si tu pedido llega antes del plazo estimado, "
                "nos comunicaremos contigo para coordinar la entrega."
            )

        # =====================================
        # Envíos
        # =====================================

        if "envio" in topics:

            respuestas.append(
                "🚚 Realizamos envíos a todo el Perú.\n\n"
                "✅ Lima Metropolitana: Envío gratuito.\n"
                "✅ Provincias de Lima y demás departamentos: S/ 40."
            )

        # =====================================
        # Métodos de pago
        # =====================================

        if "pagos" in topics:

            respuestas.append(
                "💳 Aceptamos los siguientes métodos de pago:\n\n"
                "• Transferencia bancaria.\n"
                "• Depósito bancario.\n"
                "• Plin.\n"
                "• Tarjeta de crédito (6% de recargo)."
            )

        # =====================================
        # Confianza y garantía
        # =====================================

        if "confianza" in topics:

            respuestas.append(
                "✅ Somos 100% confiables. Todos nuestros productos son "
                "originales y cuentan con garantía por fallas de fábrica.\n\n"
                "⭐ Puedes ver algunas reseñas de nuestros clientes en "
                "Google Business:\n"
                "https://share.google/O6swfTMLlEd5qBDqX"
            )

        # =====================================
        # Marcas
        # =====================================

        if "marcas" in topics:

            respuestas.append(
                "🏷️ Trabajamos con una amplia selección de marcas originales.\n\n"
                "Puedes ver todas las marcas disponibles aquí:\n\n"
                f"{self.brand_service.obtener_url_marcas()}\n\n"
                "Si te interesa alguna marca en particular, "
                "dime cuál y con gusto te ayudaré."
            )

        if respuestas:

            return "\n\n".join(respuestas)

        return None
