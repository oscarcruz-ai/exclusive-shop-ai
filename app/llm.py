from app.config import GOOGLE_API_KEY


def get_llm():
    """Crea el cliente de Gemini solo cuando se necesita."""
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY no está configurada")

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )
