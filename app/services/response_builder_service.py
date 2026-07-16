from app.constants.response_constants import (
    TIEMPO_ENTREGA,
    ENVIOS,
    ORIGINALIDAD,
    GARANTIA,
    CTA_PRODUCTO,
    CTA_MARCA,
    CTA_CATEGORIA,
)


class ResponseBuilderService:

    # =====================================
    # Producto
    # =====================================

    def producto(self, nombre, url):

        return (
            f"✅ Sí, tenemos disponible el {nombre}.\n\n"
            "🔗 Puedes ver toda la información aquí:\n"
            f"{url}\n\n"
            f"{TIEMPO_ENTREGA}\n\n"
            f"{ENVIOS}\n\n"
            f"{ORIGINALIDAD}\n\n"
            f"{GARANTIA}\n\n"
            f"{CTA_PRODUCTO}"
        )

    # =====================================
    # Marca
    # =====================================

    def marca(self, marca, url):

        return (
            f"👟 Tenemos una amplia colección de productos {marca}.\n\n"
            "Puedes ver todos los modelos disponibles aquí:\n\n"
            f"{url}\n\n"
            f"{TIEMPO_ENTREGA}\n\n"
            f"{ENVIOS}\n\n"
            f"{ORIGINALIDAD}\n\n"
            f"{CTA_MARCA.format(marca=marca)}"
        )

    # =====================================
    # Categoría
    # =====================================

    def categoria(self, categoria, url):

        return (
            f"👟 Tenemos una amplia colección de {categoria}.\n\n"
            "Puedes ver todos los modelos disponibles aquí:\n\n"
            f"{url}\n\n"
            f"{TIEMPO_ENTREGA}\n\n"
            f"{ENVIOS}\n\n"
            f"{ORIGINALIDAD}\n\n"
            f"{CTA_CATEGORIA}"
        )