from app.constants.faq_patterns import FAQ_PATTERNS
from app.utils.text_utils import normalizar_texto


class TopicDetector:

    def detectar(self, pregunta):

        texto = normalizar_texto(pregunta)

        topics = set()

        # =====================================
        # Detectar mediante FAQ_PATTERNS
        # =====================================

        for topic, patrones in FAQ_PATTERNS.items():

            for patron in patrones:

                patron_normalizado = normalizar_texto(patron)

                if patron_normalizado in texto:

                    topics.add(topic)

                    break

        # =====================================
        # Reglas inteligentes
        # =====================================

        if any(
            palabra in texto
            for palabra in [
                "demora",
                "demorar",
                "tarda",
                "tardar",
                "llega",
                "llegar",
                "recibire",
                "recibiré",
                "tiempo"
            ]
        ):

            topics.add("tiempo_entrega")

        if any(
            palabra in texto
            for palabra in [
                "envio",
                "envío",
                "delivery",
                "provincia",
                "provincias"
            ]
        ):

            topics.add("envio")

        return topics
