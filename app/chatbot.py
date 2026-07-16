from langchain_core.messages import HumanMessage, AIMessage

from app.router.query_router import QueryRouter
from app.logger import logger


class ExclusiveShopBot:

    def __init__(self):

        self.historial = []

        self.router = QueryRouter()

    def responder(
        self,
        pregunta,
        intent="general",
        pregunta_original=None
    ):

        # Si no se envía la pregunta original,
        # usamos la misma pregunta.

        if pregunta_original is None:
            pregunta_original = pregunta

        historial_texto = "\n".join(
            [
                f"Cliente: {m.content}"
                if isinstance(m, HumanMessage)
                else f"Asistente: {m.content}"
                for m in self.historial
            ]
        )

        try:

            logger.info(
                "Procesando consulta del usuario..."
            )

            respuesta = self.router.responder(
                pregunta=pregunta,
                historial=historial_texto,
                intent=intent
            )

            logger.info(
                "Respuesta generada correctamente."
            )

        except Exception as e:

            logger.exception(
                "Error procesando la consulta."
            )

            mensaje = str(e).upper()

            if "GOOGLE_API_KEY" in mensaje:
                return (
                    "El asistente de IA no está configurado todavía. "
                    "Puedes consultar el catálogo, marcas, envíos y tiempos de entrega."
                )

            if "RESOURCE_EXHAUSTED" in mensaje or "429" in mensaje:

                logger.warning(
                    "Límite de solicitudes de IA alcanzado."
                )

                return (
                    "⚠️ En este momento el servicio de IA alcanzó el límite de solicitudes.\n\n"
                    "Por favor intenta nuevamente en aproximadamente un minuto."
                )

            return (
                "⚠️ Ocurrió un error al procesar tu consulta.\n\n"
                "Por favor intenta nuevamente."
            )

        # Guardar conversación con la pregunta REAL del usuario

        self.historial.append(
            HumanMessage(content=pregunta_original)
        )

        self.historial.append(
            AIMessage(content=respuesta)
        )

        logger.info(
            "Conversación almacenada en el historial."
        )

        return respuesta
