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

    def responder(
        self,
        pregunta,
        historial="",
        intent="general"
    ):

        logger.info(f"Pregunta recibida: {pregunta}")

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

            return self._preguntar_rag(pregunta, historial, intent)

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

        return self._preguntar_rag(pregunta, historial, intent)
