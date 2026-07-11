import pandas as pd

from app.config import (
    CATALOGO_PATH,
    CSV_COLUMNS,
)


class CatalogService:

    def __init__(self):
        self.df = pd.read_csv(CATALOGO_PATH)

    # ==========================
    # Información general
    # ==========================

    def obtener_productos(self):
        return self.df.copy()

    def obtener_nombres_productos(self):

        productos = (
            self.df[CSV_COLUMNS["name"]]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        return sorted(productos)

    def obtener_marcas(self):

        marcas = (
            self.df[CSV_COLUMNS["brand"]]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        return sorted(marcas)

    def obtener_marcas_normalizadas(self):

        marcas = {}

        for valor in self.obtener_marcas():

            for marca in valor.split(","):

                marca = marca.strip()

                if not marca:
                    continue

                variantes = [
                    marca.lower(),
                    marca.lower().replace("-", ""),
                    marca.lower().replace(" ", ""),
                    marca.lower().replace("-", "").replace(" ", "")
                ]

                for variante in variantes:
                    marcas[variante] = marca

        return marcas

    def obtener_categorias(self):

        categorias = (
            self.df[CSV_COLUMNS["category"]]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        return sorted(categorias)

    def obtener_categorias_limpias(self):

        categorias = set()

        for valor in self.df[CSV_COLUMNS["category"]].dropna():

            bloques = str(valor).split("|")

            for bloque in bloques:

                niveles = bloque.split(">")

                for nivel in niveles:

                    categoria = nivel.strip()

                    if (
                        categoria
                        and categoria.lower() != "sin categorizar"
                    ):
                        categorias.add(categoria.title())

        return sorted(categorias)

    # ==========================
    # Búsquedas
    # ==========================

    def buscar_producto(self, nombre):

        nombre = nombre.lower()

        resultados = self.df[
            self.df[CSV_COLUMNS["name"]]
            .astype(str)
            .str.lower()
            .str.contains(nombre, na=False)
        ]

        return resultados

    def obtener_productos_por_marca(self, marca):

        marca = marca.lower()

        resultados = self.df[
            self.df[CSV_COLUMNS["brand"]]
            .astype(str)
            .str.lower()
            .str.contains(marca, na=False)
        ]

        return resultados

    def obtener_productos_por_categoria(self, categoria):

        categoria = categoria.lower()

        resultados = self.df[
            self.df[CSV_COLUMNS["category"]]
            .astype(str)
            .str.lower()
            .str.contains(categoria, na=False)
        ]

        return resultados
    
    def detectar_marcas(self, texto):

        texto_normalizado = (
            texto.lower()
            .replace("-", "")
            .replace(" ", "")
        )

        marcas_encontradas = []

        for clave, marca in self.obtener_marcas_normalizadas().items():

            if clave in texto_normalizado:

                if marca not in marcas_encontradas:
                    marcas_encontradas.append(marca)

        return marcas_encontradas