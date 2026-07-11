from app.services.catalog_service import CatalogService


BASE_URL = "https://www.exclusiveshopperu.com"


class CatalogAdvisor:

    def __init__(self):
        self.catalog = CatalogService()

    def responder_categoria(self, categoria):

        marcas = self.catalog.obtener_marcas_por_categoria(categoria)

        respuesta = (
            f"👟 Tenemos una gran variedad de {categoria.lower()} exclusivas.\n\n"
            f"Puedes explorar la categoría aquí:\n"
            f"{BASE_URL}/categoria/{categoria.lower().replace(' ', '-')}/\n\n"
        )

        if marcas:

            respuesta += "Trabajamos con marcas como:\n\n"

            for marca in marcas[:8]:
                respuesta += f"• {marca}\n"

            respuesta += "\n¿Qué marca te interesa?"

        return respuesta

    def responder_marca(self, marca):

        productos = self.catalog.obtener_productos_por_marca(marca)

        if productos.empty:
            return None

        nombres = (
            productos["Nombre"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        respuesta = (
            f"👟 Tenemos una amplia colección de {marca}.\n\n"
            f"Puedes verla aquí:\n"
            f"{BASE_URL}/categoria/zapatillas/{marca.lower().replace(' ', '-').replace('&','').replace('--','-')}/\n\n"
        )

        respuesta += "Algunos modelos disponibles son:\n\n"

        for nombre in nombres[:5]:
            respuesta += f"• {nombre}\n"

        if len(nombres) > 5:
            respuesta += f"\n...y {len(nombres)-5} modelos más."

        respuesta += f"\n\n¿Qué modelo {marca} buscas?"

        return respuesta