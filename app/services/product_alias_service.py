from app.services.catalog_service import CatalogService
from app.utils.text_utils import normalizar_texto


PALABRAS_IGNORAR = {
    "ray",
    "ban",
    "meta",

    "nike",
    "adidas",
    "jordan",
    "apple",

    "low",
    "mid",
    "high",
    "og",
    "sp",
    "se",

    "gen",

    "x",
}


class ProductAliasService:

    def __init__(self):

        self.catalog = CatalogService()

        self.aliases = self._crear_aliases()

    def obtener_aliases(self):

        return self.aliases

    def _crear_aliases(self):

        aliases = {}

        productos = self.catalog.obtener_nombres_productos()

        for producto in productos:

            nombre = normalizar_texto(producto)

            nombre = (
                nombre
                .replace("(", "")
                .replace(")", "")
                .replace("-", " ")
            )

            palabras = [
                p
                for p in nombre.split()
                if p
            ]

            # ----------------------------------
            # Alias = nombre completo
            # ----------------------------------

            aliases.setdefault(
                nombre,
                producto
            )

            # ----------------------------------
            # Alias = palabras individuales
            # ----------------------------------

            palabras_utiles = []

            for palabra in palabras:

                if len(palabra) < 3:
                    continue

                if palabra in PALABRAS_IGNORAR:
                    continue

                palabras_utiles.append(palabra)

                aliases.setdefault(
                    palabra,
                    producto
                )

            # ----------------------------------
            # Alias de dos palabras
            # ----------------------------------

            for i in range(len(palabras_utiles)-1):

                alias = (
                    palabras_utiles[i]
                    + " "
                    + palabras_utiles[i+1]
                )

                aliases.setdefault(
                    alias,
                    producto
                )

            # ----------------------------------
            # Alias de tres palabras
            # ----------------------------------

            for i in range(len(palabras_utiles)-2):

                alias = (
                    palabras_utiles[i]
                    + " "
                    + palabras_utiles[i+1]
                    + " "
                    + palabras_utiles[i+2]
                )

                aliases.setdefault(
                    alias,
                    producto
                )

        return aliases