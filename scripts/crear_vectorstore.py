from pathlib import Path

from app.embeddings import embeddings
from app.loaders.loader import cargar_documentos
from app.vectorstore import (
    crear_vectorstore,
    guardar_vectorstore,
)

ruta_csv = Path("data/catalogo/catalogo_exclusive_shop_ai_v2.csv")

carpeta_pdf = Path("data/documentos")

documentos = cargar_documentos(
    ruta_csv,
    carpeta_pdf
)

print(f"Documentos cargados: {len(documentos)}")

vectorstore = crear_vectorstore(
    documentos,
    embeddings
)

guardar_vectorstore(
    vectorstore,
    "data/vector_db"
)

print("✅ Base vectorial guardada correctamente")