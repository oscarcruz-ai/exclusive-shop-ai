from app.config import VECTOR_DB_DIR
from app.embeddings import embeddings
from app.vectorstore import cargar_vectorstore

vectorstore = cargar_vectorstore(
    VECTOR_DB_DIR,
    embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5
    }
)