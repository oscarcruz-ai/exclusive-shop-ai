from app.services.brand_service import BrandService

class ConversationManager:

    BASE_URL = "https://www.exclusiveshopperu.com"

    def __init__(self):
        self.brand_service = BrandService()

    CATEGORY_URLS = {
        "zapatillas": "/categoria/zapatillas/",
        "lentes": "/categoria/smart-glasses/",
        "smart glasses": "/categoria/smart-glasses/",
        "ropa": "/categoria/ropa/",
        "relojes": "/categoria/relojes/",
        "perfumes": "/categoria/perfumes/",
        "apple": "/categoria/apple/",
    }

    def responder(self, pregunta, intent, entidades):

        texto = pregunta.lower().strip()

        categorias = entidades.get("categories", [])
        marcas = entidades.get("brands", [])
        productos = entidades.get("products", [])

        # ==========================================
        # CONSULTAS GENERALES
        # ==========================================

        if intent == "price" and not productos:
            return "💰 Claro. ¿De qué producto deseas conocer el precio?"

        if texto in ["talla", "tallas", "size"]:
            return "📏 ¿De qué producto necesitas conocer la talla?"

        if texto in ["stock", "disponible", "disponibilidad"]:
            return "📦 ¿Qué producto deseas consultar?"

        if texto in ["nuevo", "nuevos", "modelos nuevos", "novedades"]:
            return "🆕 ¿De qué categoría o marca deseas ver las novedades?"

        # ==========================================
        # YA EXISTE UN PRODUCTO
        # ==========================================

        if productos:
            return None

        # ==========================================
        # CATEGORÍA + MARCA
        # ==========================================

        if len(categorias) == 1 and len(marcas) == 1:

            categoria = categorias[0]
            marca = marcas[0]

            # Apple

            if marca.lower() == "apple":

                return (
                    "🍎 ¡Excelente elección!\n\n"
                    "Tenemos una amplia colección de productos Apple.\n\n"
                    "🔗 Explóralos aquí:\n"
                    f"{self.BASE_URL}/categoria/apple/\n\n"
                    "¿Qué producto Apple estás buscando?\n\n"
                    "• iPhone\n"
                    "• Apple Watch\n"
                    "• AirPods\n"
                    "• iPad\n"
                    "• MacBook"
                )

            # Ray-Ban

            if (
                categoria.lower() == "lentes"
                and marca.lower() in ["ray-ban", "ray ban"]
            ):

                return (
                    "🕶️ ¡Perfecto!\n\n"
                    "Tenemos toda la colección Ray-Ban.\n\n"
                    "🔗 Puedes verla aquí:\n"
                    f"{self.BASE_URL}/categoria/smart-glasses/\n\n"
                    "¿Qué modelo buscas?\n\n"
                    "• Wayfarer\n"
                    "• Headliner\n"
                    "• Skyler"
                )

            slug = (
                marca.lower()
                .replace("&", "")
                .replace(" ", "-")
                .replace("--", "-")
            )

            categoria_slug = (
                categoria.lower()
                .replace(" ", "-")
            )

            return (
                f"👟 Tenemos una amplia colección de {categoria.lower()} {marca}.\n\n"
                "🔗 Explora todos los modelos aquí:\n"
                f"{self.BASE_URL}/categoria/{categoria_slug}/{slug}/\n\n"
                f"¿Qué modelo {marca} estás buscando?"
            )

        # ==========================================
        # SOLO CATEGORÍA
        # ==========================================

        if len(categorias) == 1 and not marcas:

            categoria = categorias[0]

            url = self.CATEGORY_URLS.get(
                categoria.lower(),
                ""
            )

            respuesta = (
                "✨ ¡Excelente elección!\n\n"
                f"Tenemos una amplia colección de {categoria} exclusivas.\n\n"
            )

            if url:

                respuesta += (
                    "🔗 Explora la colección aquí:\n"
                    f"{self.BASE_URL}{url}\n\n"
                )

            if categoria.lower() == "zapatillas":

                respuesta += (
                    "¿Qué marca estás buscando?\n\n"
                    "Algunas de nuestras marcas son:\n"
                    "• Nike\n"
                    "• Jordan\n"
                    "• Off-White\n"
                    "• Supreme\n"
                    "• Louis Vuitton"
                )

            else:

                respuesta += (
                    "¿Qué marca o modelo estás buscando?"
                )

            return respuesta

        # ==========================================
        # MARCA + TEXTO ADICIONAL
        # ==========================================

        if len(marcas) == 1 and not productos:

            marca = marcas[0]

            texto_norm = texto.lower()

            if texto_norm != marca.lower():

                url = self.brand_service.obtener_url(marca)

                return (
                    f"👟 Tenemos una amplia colección de productos {marca}.\n\n"
                    "Puedes ver todos los modelos disponibles aquí:\n\n"
                    f"{url}\n\n"
                    "📦 Tiempo estimado de entrega: 16 a 18 días hábiles.\n\n"
                    "🚚 Realizamos envíos a todo el Perú.\n\n"
                    "✅ Todos nuestros productos son 100% originales.\n\n"
                    "¿Puedo ayudarte con algún otro producto o tienes alguna otra consulta?"
                )

        # ==========================================
        # SOLO MARCA
        # ==========================================

        if len(marcas) == 1 and not categorias:

            marca = marcas[0]
            marca_lower = marca.lower()

            # Apple

            if marca_lower == "apple":

                return (
                    "🍎 ¡Excelente elección!\n\n"
                    "Tenemos una amplia colección de productos Apple.\n\n"
                    "🔗 Explóralos aquí:\n"
                    f"{self.BASE_URL}/categoria/apple/\n\n"
                    "¿Qué producto Apple estás buscando?\n\n"
                    "• iPhone\n"
                    "• Apple Watch\n"
                    "• AirPods\n"
                    "• iPad\n"
                    "• MacBook"
                )

            # Ray-Ban

            if marca_lower in ["ray-ban", "ray ban"]:

                return (
                    "🕶️ ¡Excelente elección!\n\n"
                    "Tenemos una amplia colección de lentes Ray-Ban.\n\n"
                    "🔗 Explóralos aquí:\n"
                    f"{self.BASE_URL}/categoria/smart-glasses/\n\n"
                    "¿Qué modelo Ray-Ban estás buscando?"
                )

            # Meta

            if marca_lower == "meta":

                return (
                    "🥽 ¿Buscas Ray-Ban Meta o Meta Quest?"
                )

            # Las marcas normales se resuelven en CatalogSearchService, que
            # conoce la URL real del catálogo y usa un cierre consistente.
            return None

        # ==========================================
        # VARIAS MARCAS
        # ==========================================

        if len(marcas) > 1:

            marcas_lower = [
                m.lower()
                for m in marcas
            ]

            if (
                "ray-ban" in marcas_lower
                and "meta" in marcas_lower
            ):

                return (
                    "🕶️ ¡Perfecto!\n\n"
                    "Tenemos toda la colección Ray-Ban Meta.\n\n"
                    "🔗 Puedes verla aquí:\n"
                    f"{self.BASE_URL}/categoria/smart-glasses/\n\n"
                    "¿Qué modelo buscas?\n\n"
                    "• Wayfarer\n"
                    "• Headliner\n"
                    "• Skyler"
                )

            return (
                "🙂 Encontré productos relacionados con esas marcas.\n\n"
                "¿Hay algún modelo específico que estés buscando?"
            )

        # ==========================================
        # SIN INFORMACIÓN SUFICIENTE
        # ==========================================

        return None
