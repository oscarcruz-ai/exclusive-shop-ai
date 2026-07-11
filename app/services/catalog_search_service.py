from app.services.catalog_service import CatalogService
from app.utils.text_utils import normalizar_texto


class CatalogSearchService:

    BASE_URL = "https://www.exclusiveshopperu.com"

    def __init__(self):

        self.catalog = CatalogService()

        # Últimas opciones mostradas al usuario
        self.last_options = []

    # ==========================================
    # Buscar
    # ==========================================

    def buscar(self, entidades):

        df = self.catalog.obtener_productos()

        # Categoría

        if entidades["categories"]:

            categoria = normalizar_texto(
                entidades["categories"][0]
            )

            df = df[
                df["Categorías limpias"]
                .fillna("")
                .apply(normalizar_texto)
                .str.contains(categoria)
            ]

        # Marca

        if entidades["brands"]:

            marca = normalizar_texto(
                entidades["brands"][0]
            )

            df = df[
                df["Marcas"]
                .fillna("")
                .apply(normalizar_texto)
                .str.contains(marca)
            ]

        # Producto

        if entidades["products"]:

            producto = normalizar_texto(
                entidades["products"][0]
            )

            df = df[
                df["Nombre"]
                .fillna("")
                .apply(normalizar_texto)
                .str.contains(producto)
            ]

        return df

    # ==========================================
    # Buscar dentro de las últimas opciones
    # ==========================================

    def buscar_en_ultimas_opciones(self, texto):

        if not self.last_options:
            return None

        texto = normalizar_texto(texto)

        coincidencias = []

        for nombre in self.last_options:

            if texto in normalizar_texto(nombre):
                coincidencias.append(nombre)

        if len(coincidencias) == 1:
            return coincidencias[0]

        return None

    # ==========================================
    # Responder
    # ==========================================

    def responder(self, entidades):

        resultados = self.buscar(entidades)

        if resultados.empty:

            self.last_options = []

            return None

        # ======================================
        # Coincidencia exacta
        # ======================================

        if entidades["products"]:

            producto_buscado = normalizar_texto(
                entidades["products"][0]
            )

            coincidencia = resultados[
                resultados["Nombre"]
                .fillna("")
                .apply(normalizar_texto)
                == producto_buscado
            ]

            if not coincidencia.empty:

                producto = coincidencia.iloc[0]

                respuesta = (
                    "✅ ¡Lo encontré!\n\n"
                    f"{producto['Nombre']}"
                )

                if (
                    "URL" in producto.index
                    and str(producto["URL"]).strip()
                ):

                    respuesta += (
                        "\n\n🔗 Ver producto:\n"
                        f"{producto['URL']}"
                    )

                self.last_options = []

                return respuesta

        # ======================================
        # Solo un resultado
        # ======================================

        if len(resultados) == 1:

            producto = resultados.iloc[0]

            respuesta = (
                "✅ ¡Lo encontré!\n\n"
                f"{producto['Nombre']}"
            )

            if (
                "URL" in producto.index
                and str(producto["URL"]).strip()
            ):

                respuesta += (
                    "\n\n🔗 Ver producto:\n"
                    f"{producto['URL']}"
                )

            self.last_options = []

            return respuesta

        # ======================================
        # Solo marca
        # ======================================

        if entidades["brands"] and not entidades["products"]:

            self.last_options = []

            marca = entidades["brands"][0]

            slug = (
                marca.lower()
                .replace("&", "")
                .replace(" ", "-")
            )

            return (
                f"👟 Tenemos una amplia colección de {marca}.\n\n"
                "🔗 Explora todos los modelos aquí:\n"
                f"{self.BASE_URL}/categoria/zapatillas/{slug}/\n\n"
                f"¿Qué modelo {marca} estás buscando?"
            )

        # ======================================
        # Varias opciones
        # ======================================

        nombres = (
            resultados["Nombre"]
            .dropna()
            .drop_duplicates()
            .tolist()
        )

        # Guardar las opciones para la siguiente pregunta
        self.last_options = nombres

        respuesta = (
            "🔎 Encontré varios modelos relacionados.\n\n"
        )

        respuesta += (
            "Estas son las opciones disponibles:\n\n"
        )

        for nombre in nombres:

            respuesta += f"• {nombre}\n"

        respuesta += (
            "\n¿Cuál de ellos te interesa?\n"
            "Puedes escribirme el nombre completo o parte del nombre."
        )

        return respuesta