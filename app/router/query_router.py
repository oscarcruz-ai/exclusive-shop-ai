import re

from app.services.product_detector import ProductDetector
from app.services.catalog_search_service import CatalogSearchService
from app.services.intent_detector import IntentDetector
from app.services.faq_service import FAQService
from app.logger import logger


class QueryRouter:

    def __init__(self):

        self.detector = ProductDetector()
        self.catalog = CatalogSearchService()
        self.intent_detector = IntentDetector()
        self.faq = FAQService()

    @staticmethod
    def _preguntar_rag(pregunta, historial, intent):
        # El modelo de embeddings puede requerir una descarga. Importarlo solo
        # para consultas que realmente necesitan RAG evita que bloquee todo el
        # chat (saludos, catálogo y preguntas frecuentes incluidos).
        from app.rag import preguntar

        return preguntar(
            pregunta=pregunta,
            historial=historial,
            intent=intent,
        )

    def _es_saludo(self, pregunta: str) -> bool:

        texto = pregunta.lower().strip()

        texto = re.sub(
            r"[^\wáéíóúüñ\s]",
            "",
            texto
        )

        # Detecta: hola, holaa, holaaa, holaaaa...
        if re.fullmatch(r"hola+", texto):
            return True

        saludos = {
            "buenas",
            "buenos dias",
            "buenos días",
            "buenas tardes",
            "buenas noches",
            "hey",
            "hi",
            "hello"
        }

        return texto in saludos

    def _es_consulta_invalida(self, pregunta: str) -> bool:

        texto = pregunta.strip()

        if not texto:
            return True

        # Solo emojis, signos o caracteres especiales
        if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", texto):
            return True

        return False

    def responder(
        self,
        pregunta,
        historial="",
        intent="general"
    ):

        logger.info(f"Pregunta recibida: {pregunta}")

        # =====================================
        # Saludos
        # =====================================

        if self._es_saludo(pregunta):

            logger.info("Saludo detectado")

            return (
                "¡Hola! 👋\n\n"
                "Soy el asistente inteligente de Exclusive Shop.\n\n"
                "Puedo ayudarte a encontrar productos, comparar modelos y responder dudas sobre envíos, pagos y garantías.\n\n"
                "¿Qué producto estás buscando hoy?"
            )

        # =====================================
        # Consulta inválida
        # =====================================

        if self._es_consulta_invalida(pregunta):

            logger.info("Consulta inválida")

            return (
                "No pude identificar tu consulta. 😊\n\n"
                "Puedo ayudarte con:\n\n"
                "• Productos\n"
                "• Marcas\n"
                "• Comparaciones\n"
                "• Envíos\n"
                "• Métodos de pago\n"
                "• Garantías\n\n"
                "¿Qué deseas buscar?"
            )

        # =====================================
        # Preguntas frecuentes
        # =====================================

        respuesta = self.faq.responder(
            pregunta
        )

        if respuesta:

            logger.info("Respuesta obtenida desde FAQService")

            return respuesta

        # =====================================
        # Detectar intención
        # =====================================

        tipo = self.intent_detector.detectar(
            pregunta
        )

        logger.info(
            f"Intent detectado: {tipo}"
        )

        # =====================================
        # Si es una consulta informativa,
        # usar directamente el RAG
        # =====================================

        if tipo == "information":

            logger.info(
                "Consulta enviada al RAG"
            )

            return self._preguntar_rag(
                pregunta,
                historial,
                intent
            )

        # =====================================
        # Detectar entidades
        # =====================================

        entidades = self.detector.detectar(
            pregunta
        )

        logger.info(
            f"Entidades detectadas: {entidades}"
        )

        # =====================================
        # Buscar en el catálogo
        # =====================================

        if (
            entidades["brands"]
            or entidades["products"]
            or entidades["categories"]
        ):

            respuesta = self.catalog.responder(
                entidades
            )

            if respuesta:

                logger.info(
                    "Respuesta obtenida desde CatalogSearchService"
                )

                return respuesta

        # =====================================
        # Si no encontró nada,
        # responder con el RAG
        # =====================================

        logger.info(
            "No hubo coincidencias en el catálogo. Se consulta el RAG."
        )

        return self._preguntar_rag(
            pregunta,
            historial,
            intent
        )
