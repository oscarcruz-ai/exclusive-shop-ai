from app.llm import get_llm
from app.prompts.prompt_builder import construir_prompt
from app.retrievers.smart_retriever import SmartRetriever
from app.logger import logger

smart_retriever = SmartRetriever()


def preguntar(pregunta, historial="", intent="general"):
    """
    Busca documentos relevantes y genera una respuesta con Gemini.
    """

    logger.info(f"Consulta enviada al RAG: {pregunta}")

    # ==========================================
    # Recuperar documentos
    # ==========================================

    documentos = smart_retriever.buscar(
        pregunta,
        intent
    )

    logger.info(
        f"Documentos encontrados: {len(documentos)}"
    )

    for i, doc in enumerate(documentos, start=1):

        logger.info(
            f"Documento {i}"
        )

        logger.info(
            f"Metadata: {doc.metadata}"
        )

        contenido = doc.page_content

        logger.info(
            f"Tamaño del documento: {len(contenido)} caracteres"
        )

        if len(contenido) > 500:

            logger.info(
                contenido[:500] + "..."
            )

        else:

            logger.info(
                contenido
            )

    # ==========================================
    # Construir contexto
    # ==========================================

    contexto = "\n\n".join(
        doc.page_content
        for doc in documentos
    )

    logger.info(
        f"Tamaño del contexto: {len(contexto)} caracteres"
    )

    # ==========================================
    # Construir prompt
    # ==========================================

    prompt = construir_prompt(
        contexto=contexto,
        pregunta=pregunta,
        historial=historial
    )

    logger.info(
        f"Tamaño del prompt: {len(prompt)} caracteres"
    )

    logger.info(
        f"Primeros 1500 caracteres del contexto:\n{contexto[:1500]}"
    )

    # ==========================================
    # Llamar al LLM
    # ==========================================

    respuesta = get_llm().invoke(prompt)

    logger.info(
        "Respuesta generada por Gemini."
    )

    return respuesta.content
