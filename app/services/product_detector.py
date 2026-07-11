from app.services.catalog_service import CatalogService
from app.utils.text_utils import normalizar_texto


SINONIMOS_CATEGORIAS = {
    "zapatilla": "Zapatillas",
    "zapatillas": "Zapatillas",
    "tenis": "Zapatillas",
    "sneaker": "Zapatillas",
    "sneakers": "Zapatillas",

    "reloj": "Relojes",
    "relojes": "Relojes",
    "watch": "Relojes",
    "watches": "Relojes",

    "lente": "Lentes",
    "lentes": "Lentes",
    "gafa": "Lentes",
    "gafas": "Lentes",
    "anteojos": "Lentes",

    "polera": "Ropa",
    "poleras": "Ropa",
    "polo": "Ropa",
    "polos": "Ropa",
    "camiseta": "Ropa",
    "camisetas": "Ropa",
    "casaca": "Ropa",
    "casacas": "Ropa",
    "hoodie": "Ropa",
    "ropa": "Ropa",

    "iphone": "Apple",
    "ipad": "Apple",
    "macbook": "Apple",
    "airpods": "Apple",
    "apple watch": "Apple",
}


APPLE_PRODUCTOS = {
    "iphone": "iPhone",
    "ipad": "iPad",
    "airpods": "AirPods",
    "macbook": "MacBook",
    "apple watch": "Apple Watch",
}


MODELOS_RAYBAN_META = {
    "wayfarer": "Ray-Ban Meta Wayfarer",
    "headliner": "Ray-Ban Meta Headliner",
    "skyler": "Ray-Ban Meta Skyler",
}


class ProductDetector:

    def __init__(self):
        self.catalog = CatalogService()

    def detectar(self, texto):

        texto_normalizado = normalizar_texto(texto)

        resultado = {
            "brands": [],
            "products": [],
            "categories": []
        }

        # =====================================
        # Detectar marcas
        # =====================================

        resultado["brands"] = self.catalog.detectar_marcas(texto)

        # =====================================
        # Detectar productos completos
        # =====================================

        productos_detectados = []

        for producto in self.catalog.obtener_nombres_productos():

            producto_normalizado = normalizar_texto(producto)

            if producto_normalizado in texto_normalizado:
                productos_detectados.append(producto)

        productos_detectados = list(set(productos_detectados))

        productos_detectados.sort(
            key=len,
            reverse=True
        )

        if productos_detectados:

            resultado["products"] = [
                productos_detectados[0]
            ]

        # =====================================
        # Detectar categorías
        # =====================================

        marcas = {
            normalizar_texto(m)
            for m in self.catalog.obtener_marcas()
        }

        for categoria in self.catalog.obtener_categorias_limpias():

            categoria_normalizada = normalizar_texto(categoria)

            if categoria_normalizada in marcas:
                continue

            if categoria_normalizada in texto_normalizado:

                if categoria not in resultado["categories"]:
                    resultado["categories"].append(categoria)

        # =====================================
        # Detectar sinónimos
        # =====================================

        for palabra, categoria in SINONIMOS_CATEGORIAS.items():

            if palabra not in texto_normalizado:
                continue

            # -----------------------------
            # Apple
            # -----------------------------

            if categoria == "Apple":

                if "Apple" not in resultado["brands"]:
                    resultado["brands"].append("Apple")

                if not resultado["products"]:

                    if palabra in APPLE_PRODUCTOS:

                        resultado["products"].append(
                            APPLE_PRODUCTOS[palabra]
                        )

            # -----------------------------
            # Otras categorías
            # -----------------------------

            else:

                if categoria not in resultado["categories"]:

                    resultado["categories"].append(
                        categoria
                    )

        # =====================================
        # Modelos Ray-Ban Meta
        # =====================================

        marcas_lower = [
            marca.lower()
            for marca in resultado["brands"]
        ]

        if (
            "meta" in marcas_lower
            or "ray-ban" in marcas_lower
            or "ray ban" in marcas_lower
        ):

            for palabra, producto in MODELOS_RAYBAN_META.items():

                if palabra in texto_normalizado:

                    resultado["products"] = [producto]
                    break

        # =====================================
        # Conservar solo el producto
        # más específico
        # =====================================

        if resultado["products"]:

            resultado["products"] = sorted(
                list(set(resultado["products"])),
                key=len,
                reverse=True
            )

            resultado["products"] = [
                resultado["products"][0]
            ]

        return resultado