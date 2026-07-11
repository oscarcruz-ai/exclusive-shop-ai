from app.utils.text_utils import normalizar_texto

BASE_URL = "https://www.exclusiveshopperu.com"


class UrlBuilder:

    CATEGORY_URLS = {
        "zapatillas": "/categoria/zapatillas/",
        "lentes": "/categoria/smart-glasses/",
        "smart glasses": "/categoria/smart-glasses/",
        "smartglasses": "/categoria/smart-glasses/",
        "relojes": "/categoria/relojes/",
        "ropa": "/categoria/ropa/",
        "perfumes": "/categoria/perfumes/",
        "apple": "/categoria/apple/",
        "skincare": "/categoria/skincare/",
    }

    @classmethod
    def categoria(cls, categoria):

        categoria = normalizar_texto(categoria)

        ruta = cls.CATEGORY_URLS.get(categoria)

        if ruta:
            return BASE_URL + ruta

        return BASE_URL

    @classmethod
    def marca(cls, categoria, marca):

        categoria = normalizar_texto(categoria)
        marca = normalizar_texto(marca)

        # Zapatillas
        if categoria == "zapatillas":

            slug = (
                marca
                .replace(" ", "-")
                .replace("&", "")
            )

            return f"{BASE_URL}/categoria/zapatillas/{slug}/"

        # Smart Glasses
        if categoria in ["lentes", "smart glasses"]:

            return f"{BASE_URL}/categoria/smart-glasses/"

        # Apple
        if categoria == "apple":

            return f"{BASE_URL}/categoria/apple/"

        return BASE_URL

    @classmethod
    def producto(cls, url):

        if not url:
            return BASE_URL

        return url