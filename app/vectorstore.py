from pathlib import Path

from langchain_community.vectorstores import FAISS


def crear_vectorstore(documentos, embeddings):
    """
    Crea una base vectorial FAISS.
    """

    return FAISS.from_documents(
        documentos,
        embeddings
    )


def guardar_vectorstore(vectorstore, ruta):

    ruta = Path(ruta)

    ruta.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore.save_local(str(ruta))


def cargar_vectorstore(ruta, embeddings):

    return FAISS.load_local(
        str(ruta),
        embeddings,
        allow_dangerous_deserialization=True
    )