from app.llm import llm
from app.prompts.prompt_builder import construir_prompt
from app.retrievers.smart_retriever import SmartRetriever

smart_retriever = SmartRetriever()


def preguntar(pregunta, historial="", intent="general"):
    """
    Busca documentos relevantes y genera una respuesta con Gemini.
    """

    print("\n" + "=" * 80)
    print(f"🔎 Consulta enviada al RAG: {pregunta}")
    print("=" * 80)

    # ==========================================
    # Recuperar documentos
    # ==========================================

    documentos = smart_retriever.buscar(
        pregunta,
        intent
    )

    print(f"\n📄 Documentos encontrados: {len(documentos)}")

    for i, doc in enumerate(documentos, start=1):

        print("\n" + "-" * 60)
        print(f"Documento {i}")

        print("Metadata:")
        print(doc.metadata)

        contenido = doc.page_content

        print(f"Tamaño: {len(contenido)} caracteres")

        print("\nContenido:")

        if len(contenido) > 500:
            print(contenido[:500] + "...")
        else:
            print(contenido)

    # ==========================================
    # Construir contexto
    # ==========================================

    contexto = "\n\n".join(
        doc.page_content
        for doc in documentos
    )

    print("\n" + "=" * 80)
    print(f"📏 Tamaño del contexto: {len(contexto)} caracteres")
    print("=" * 80)

    # ==========================================
    # Construir prompt
    # ==========================================

    prompt = construir_prompt(
        contexto=contexto,
        pregunta=pregunta,
        historial=historial
    )

    print(f"📏 Tamaño del prompt: {len(prompt)} caracteres")

    print("\n📝 Primeros 1500 caracteres del contexto:\n")

    print(contexto[:1500])

    # ==========================================
    # Llamar al LLM
    # ==========================================

    respuesta = llm.invoke(prompt)

    print("\n" + "=" * 80)
    print("🤖 Respuesta Gemini")
    print("=" * 80)
    print(respuesta.content)

    return respuesta.content