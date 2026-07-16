from app.chatbot import ExclusiveShopBot
from app.agents.intent_classifier import IntentClassifier
from app.services.product_detector import ProductDetector
from app.services.catalog_search_service import CatalogSearchService
from app.services.topic_detector import TopicDetector
from app.services.brand_service import BrandService
from app.services.faq_service import FAQService
from app.utils.text_utils import normalizar_texto

from app.validators.input_validator import InputValidator
from app.advisors.small_talk_manager import SmallTalkManager
from app.advisors.conversation_manager import ConversationManager
from app.advisors.context_manager import ContextManager
from app.advisors.catalog_advisor import CatalogAdvisor


class SalesAgent:

    STOPWORDS_BUSQUEDA = {
        "quiero", "busco", "buscar", "tienen", "tiene", "de", "la",
        "el", "los", "las", "un", "una", "para", "por", "favor",
    }

    def __init__(self):

        self.chatbot = ExclusiveShopBot()

        self.intent_classifier = IntentClassifier()

        self.product_detector = ProductDetector()

        self.catalog_search = CatalogSearchService()

        # =====================================
        # NUEVO
        # =====================================

        self.topic_detector = TopicDetector()

        self.brand_service = BrandService()

        self.faq_service = FAQService()

        self.input_validator = InputValidator()

        self.small_talk_manager = SmallTalkManager()

        self.conversation_manager = ConversationManager()

        self.catalog_advisor = CatalogAdvisor()

        self.context_manager = ContextManager()

    def responder(self, pregunta):

        if not isinstance(pregunta, str):
            return "Por favor, escribe tu consulta para poder ayudarte."

        # Estas respuestas no necesitan consultar el catálogo ni la IA.
        respuesta = self.input_validator.validar(pregunta)

        if respuesta:
            return respuesta

        # Las preguntas frecuentes deben responderse antes de mezclar el
        # contexto. De lo contrario una pregunta sobre envíos, pagos o plazos
        # puede heredar el último producto consultado.
        topics = self.topic_detector.detectar(pregunta)

        if "marcas" in topics:
            return self.brand_service.responder_marcas()

        if {"tienda", "tiempo_entrega", "envio", "pagos", "confianza"} & topics:
            respuesta = self.faq_service.responder(pregunta)

            if respuesta:
                return respuesta

        respuesta = self.small_talk_manager.responder(pregunta)

        if respuesta:
            return respuesta

        # =====================================
        # Detectar intención
        # =====================================

        intent = self.intent_classifier.detectar(pregunta)

        # =====================================
        # Detectar entidades
        # =====================================

        entidades_originales = self.product_detector.detectar(pregunta)

        # =====================================
        # Detectar búsquedas parciales
        # =====================================

        MARCAS_REDIRECCION = {
            "nike",
            "adidas",
            "jordan",
            "apple",
            "ray-ban",
            "ray ban",
            "oakley",
        }

        if (
            not entidades_originales["products"]
            and (
                entidades_originales["brands"]
                or entidades_originales["categories"]
            )
        ):

            texto_normalizado = normalizar_texto(pregunta)

            if entidades_originales["brands"]:

                marca = normalizar_texto(
                    entidades_originales["brands"][0]
                )

                if (
                    marca in MARCAS_REDIRECCION
                    and texto_normalizado != marca
                ):
                    pass

                else:

                    terminos_descartados = set(self.STOPWORDS_BUSQUEDA)

                    for entidad in (
                        entidades_originales["brands"]
                        + entidades_originales["categories"]
                    ):
                        terminos_descartados.update(
                            normalizar_texto(entidad).split()
                        )

                    terminos_producto = [
                        termino
                        for termino in texto_normalizado.split()
                        if termino not in terminos_descartados
                    ]

                    if len(terminos_producto) >= 2:
                        entidades_originales["products"] = [
                            " ".join(terminos_producto)
                        ]

            else:

                terminos_descartados = set(self.STOPWORDS_BUSQUEDA)

                for entidad in entidades_originales["categories"]:
                    terminos_descartados.update(
                        normalizar_texto(entidad).split()
                    )

                terminos_producto = [
                    termino
                    for termino in texto_normalizado.split()
                    if termino not in terminos_descartados
                ]

                if len(terminos_producto) >= 2:
                    entidades_originales["products"] = [
                        " ".join(terminos_producto)
                    ]

        # =====================================
        # Completar entidades con el contexto
        # =====================================

        entidades = self.context_manager.merge(entidades_originales)

        contexto = self.context_manager.get()

        texto = pregunta.lower().strip()

        # =====================================
        # Resolver usando las últimas opciones
        # =====================================

        if not entidades["products"]:

            producto = self.catalog_search.buscar_en_ultimas_opciones(
                pregunta
            )

            if producto:

                entidades["products"] = [producto]

        # =====================================
        # Resolver modelos Ray-Ban Meta
        # =====================================

        if (
            contexto["brand"]
            and contexto["brand"].lower() in [
                "meta",
                "ray-ban",
                "ray ban",
                "ray-ban meta",
            ]
            and not entidades["products"]
        ):

            modelos = {
                "wayfarer": "Ray-Ban Meta Wayfarer",
                "headliner": "Ray-Ban Meta Headliner",
                "skyler": "Ray-Ban Meta Skyler",
            }

            if texto in modelos:

                entidades["brands"] = ["Meta"]

                entidades["products"] = [
                    modelos[texto]
                ]

        # =====================================
        # Resolver productos Apple
        # =====================================

        if (
            contexto["brand"]
            and contexto["brand"].lower() == "apple"
            and not entidades["products"]
        ):

            productos = {
                "iphone": "iPhone",
                "ipad": "iPad",
                "airpods": "AirPods",
                "apple watch": "Apple Watch",
                "macbook": "MacBook",
            }

            for palabra, producto in productos.items():

                if texto.startswith(palabra):

                    entidades["brands"] = ["Apple"]

                    entidades["products"] = [
                        producto
                    ]

                    break

        # =====================================
        # AHORA SÍ actualizamos el contexto
        # =====================================

        self.context_manager.update(entidades)

        # =====================================
        # 3. CONVERSACIÓN
        # =====================================

        respuesta = self.conversation_manager.responder(
            pregunta=pregunta,
            intent=intent,
            entidades=entidades
        )

        if respuesta:

            return respuesta

        # =====================================
        # 3.1 TOPICS (NUEVO)
        # =====================================

        if "marcas" in topics:
            return self.brand_service.responder_marcas()

        # =====================================
        # 4. ASESOR DE PRODUCTOS
        # =====================================

        respuesta = self.catalog_advisor.responder(
            pregunta
        )

        if respuesta:

            return respuesta

        # =====================================
        # 5. CATÁLOGO
        # =====================================

        respuesta = self.catalog_search.responder(entidades)

        if respuesta:

            return respuesta

        # =====================================
        # 6. RAG
        # =====================================

        consulta = self.context_manager.build_query(pregunta)

        return self.chatbot.responder(
            pregunta=consulta,
            pregunta_original=pregunta,
            intent=intent
        )
