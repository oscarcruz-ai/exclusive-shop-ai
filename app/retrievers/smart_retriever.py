from app.retriever import retriever


class SmartRetriever:

    def buscar(self, pregunta, intent="general"):

        # Por ahora simplemente usamos el retriever existente.
        # Más adelante añadiremos lógica según la intención.
        documentos = retriever.invoke(pregunta)

        return documentos