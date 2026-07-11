from langchain_core.documents import Document

from app.embeddings import embeddings
from app.vectorstore import crear_vectorstore

documentos = [
    Document(page_content="Ray-Ban Meta Wayfarer"),
    Document(page_content="Air Jordan 1 Retro High"),
    Document(page_content="Nike Dunk Low Panda"),
]

vectorstore = crear_vectorstore(documentos, embeddings)

print("✅ Base vectorial creada correctamente")
print(f"Total documentos: {vectorstore.index.ntotal}")