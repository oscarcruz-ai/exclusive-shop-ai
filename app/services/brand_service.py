from app.services.catalog_service import CatalogService
from app.config import BASE_URL


class BrandService:

    BRAND_URLS = {

        # ==========================
        # Zapatillas
        # ==========================

        "Nike": "/categoria/zapatillas/nike/",
        "Adidas": "/categoria/zapatillas/adidas/",
        "Jordan": "/categoria/zapatillas/jordan/",
        "New Balance": "/categoria/zapatillas/new-balance/",
        "Puma": "/categoria/zapatillas/puma/",
        "Asics": "/categoria/zapatillas/asics/",
        "Converse": "/categoria/zapatillas/converse/",
        "Vans": "/categoria/zapatillas/vans/",
        "Reebok": "/categoria/zapatillas/reebok/",

        # ==========================
        # Lentes
        # ==========================

        "Ray-Ban": "/categoria/lentes/ray-ban/",
        "Oakley": "/categoria/lentes/oakley/",

        # ==========================
        # Apple
        # ==========================

        "Apple": "/categoria/apple/",

        # ==========================
        # Smart Glasses
        # ==========================

        "Meta": "/categoria/smart-glasses/",

    }

    def __init__(self):

        self.catalog = CatalogService()

    def obtener_url(self, marca):

        if marca in self.BRAND_URLS:

            return f"{BASE_URL}{self.BRAND_URLS[marca]}"

        slug = (
            marca.lower()
            .replace("&", "")
            .replace(" ", "-")
        )

        return f"{BASE_URL}/marca/{slug}/"

    def obtener_marcas(self):

        df = self.catalog.obtener_productos()

        marcas = set()

        for valor in df["Marcas"].dropna().astype(str):

            for marca in valor.split(","):

                marca = marca.strip()

                if marca:

                    marcas.add(marca)

        return sorted(marcas, key=str.casefold)

    def responder_marcas(self):

        marcas = self.obtener_marcas()

        respuesta = "🏷️ Trabajamos con las siguientes marcas:\n\n"

        for marca in marcas:

            respuesta += f"• {marca}\n"

        respuesta += "\n¿Hay alguna marca que te interese?"

        return respuesta