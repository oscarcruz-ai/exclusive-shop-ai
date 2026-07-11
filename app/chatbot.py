from langchain_core.messages import HumanMessage, AIMessage

from app.rag import preguntar


class ExclusiveShopBot:

    def __init__(self):

        self.historial = []

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

            respuesta = preguntar(
                pregunta=pregunta,
                historial=historial_texto,
                intent=intent
            )

        except Exception as e:

            print("\n===== ERROR CHATBOT =====")
            print(e)
            print("=========================\n")

            mensaje = str(e).upper()

            if "RESOURCE_EXHAUSTED" in mensaje or "429" in mensaje:

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

        return respuesta