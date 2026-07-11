from app.chatbot import ExclusiveShopBot
from app.agents.intent_classifier import IntentClassifier
from app.services.product_detector import ProductDetector
from app.services.catalog_search_service import CatalogSearchService

from app.validators.input_validator import InputValidator
from app.advisors.small_talk_manager import SmallTalkManager
from app.advisors.conversation_manager import ConversationManager
from app.advisors.context_manager import ContextManager


class SalesAgent:

    def __init__(self):

        self.chatbot = ExclusiveShopBot()

        self.intent_classifier = IntentClassifier()

        self.product_detector = ProductDetector()

        self.catalog_search = CatalogSearchService()

        self.input_validator = InputValidator()

        self.small_talk_manager = SmallTalkManager()

        self.conversation_manager = ConversationManager()

        self.context_manager = ContextManager()

    def responder(self, pregunta):

        # =====================================
        # Detectar intención
        # =====================================

        intent = self.intent_classifier.detectar(pregunta)

        # =====================================
        # Detectar entidades
        # =====================================

        entidades_originales = self.product_detector.detectar(pregunta)

        print("==== DETECTOR ====")
        print(entidades_originales)

        # =====================================
        # Completar entidades con el contexto
        # =====================================

        entidades = self.context_manager.merge(entidades_originales)

        contexto = self.context_manager.get()

        print(">>> CONTEXTO ACTUAL:", contexto)

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

                print(
                    f"⭐ Producto resuelto desde last_options: {producto}"
                )

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
        # con las entidades finales
        # =====================================

        self.context_manager.update(entidades)

        print("\n===== SALES AGENT =====")
        print(f"[Intent]: {intent}")
        print(f"[Entities detectadas]: {entidades_originales}")
        print(f"[Entities finales]: {entidades}")

        self.context_manager.debug()

        # =====================================
        # 1. VALIDAR ENTRADA
        # =====================================

        respuesta = self.input_validator.validar(pregunta)

        if respuesta:

            print("✅ Respondido por InputValidator")

            return respuesta

        # =====================================
        # 2. SMALL TALK
        # =====================================

        respuesta = self.small_talk_manager.responder(pregunta)

        if respuesta:

            print("✅ Respondido por SmallTalkManager")

            return respuesta

        # =====================================
        # 3. CONVERSACIÓN
        # =====================================

        respuesta = self.conversation_manager.responder(
            pregunta=pregunta,
            intent=intent,
            entidades=entidades
        )

        if respuesta:

            print("✅ Respondido por ConversationManager")

            return respuesta

        # =====================================
        # 4. CATÁLOGO
        # =====================================

        respuesta = self.catalog_search.responder(entidades)

        if respuesta:

            print("✅ Respondido por CatalogSearchService")

            return respuesta

        # =====================================
        # 5. RAG
        # =====================================

        consulta = self.context_manager.build_query(pregunta)

        print(f"🔎 Consulta enviada al RAG: {consulta}")

        print("➡️ Consultando RAG...")

        return self.chatbot.responder(
            pregunta=consulta,
            pregunta_original=pregunta,
            intent=intent
        )