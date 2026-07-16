from app.utils.text_utils import normalizar_texto
from app.config import BASE_URL


class CategoryService:

    def obtener_slug(self, categoria: str) -> str:

        return (
            normalizar_texto(categoria)
            .replace("&", "")
            .replace(" ", "-")
        )

    def obtener_url(self, categoria: str) -> str:

        slug = self.obtener_slug(categoria)

        return (
            f"{BASE_URL}/categoria/{slug}/"
        )