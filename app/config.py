from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================================
# Variables de entorno
# ==========================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("No se encontró GOOGLE_API_KEY en el archivo .env")

# ==========================================
# Directorios
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CATALOGO_PATH = DATA_DIR / "catalogo" / "catalogo_exclusive_shop_ai_v2.csv"

DOCUMENTOS_DIR = DATA_DIR / "documentos"

VECTOR_DB_DIR = DATA_DIR / "vector_db"

# ==========================================
# Columnas del catálogo
# ==========================================

CSV_COLUMNS = {
    "name": "Nombre",
    "brand": "Marcas",
    "category": "Categorías limpias",
    "url": "URL",
    "document": "Documento IA",
}