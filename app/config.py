from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================================
# Variables de entorno
# ==========================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# La clave se valida únicamente al momento de consultar el modelo. Así el
# catálogo y las respuestas locales siguen disponibles sin servicio de IA.

# ==========================================
# Directorios
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CATALOGO_PATH = (
    DATA_DIR /
    "catalogo" /
    "catalogo_exclusive_shop_ai_v2.csv"
)

DOCUMENTOS_DIR = DATA_DIR / "documentos"

VECTOR_DB_DIR = DATA_DIR / "vector_db"

# ==========================================
# Sitio Web
# ==========================================

BASE_URL = "https://www.exclusiveshopperu.com"

# ==========================================
# Empresa
# ==========================================

EMPRESA = "Exclusive Shop"

PAIS = "Perú"

MONEDA = "S/"

# ==========================================
# Información Comercial
# ==========================================

TIEMPO_ENTREGA = "16 a 18 días hábiles"

ENVIO = "Realizamos envíos a todo el Perú."

ORIGINALIDAD = (
    "Todos nuestros productos son 100% originales."
)

GARANTIA = (
    "Garantía por fallas de fábrica."
)

# ==========================================
# IA
# ==========================================

MODEL_NAME = "gemini-2.5-flash"

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
