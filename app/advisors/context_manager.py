from copy import deepcopy


class ContextManager:

    def __init__(self):

        self.reset()

    # =====================================
    # Reiniciar contexto
    # =====================================

    def reset(self):

        self.context = {
            "category": None,
            "brand": None,
            "product": None,
            "color": None,
            "size": None,
            "options": []
        }

    # =====================================
    # Obtener contexto
    # =====================================

    def get(self):

        return deepcopy(self.context)

    # =====================================
    # Actualizar contexto
    # =====================================

    def update(self, entities):

        print(">>> UPDATE RECIBIÓ:", entities)

        categorias = entities.get("categories", [])
        marcas = entities.get("brands", [])
        productos = entities.get("products", [])

        # ---------------------------------
        # Cambio de categoría
        # ---------------------------------

        if categorias:

            categoria = categorias[0]

            if categoria != self.context["category"]:

                self.context["category"] = categoria

                # Al cambiar de categoría
                # limpiamos la información específica.

                self.context["brand"] = None
                self.context["product"] = None
                self.context["color"] = None
                self.context["size"] = None
                self.context["options"] = []

        # ---------------------------------
        # Cambio de marca
        # ---------------------------------

        if marcas:

            nueva_marca = marcas[0]

            if nueva_marca != self.context["brand"]:

                self.context["brand"] = nueva_marca
                self.context["product"] = None
                self.context["color"] = None
                self.context["size"] = None
                self.context["options"] = []

        # ---------------------------------
        # Producto
        # ---------------------------------

        if productos:

            self.context["product"] = productos[0]

            # Ya tenemos un producto concreto
            self.context["options"] = []

        # ---------------------------------
        # Debug
        # ---------------------------------

        print(">>> CONTEXTO DESPUÉS DE UPDATE:")
        print(self.context)

    # =====================================
    # Guardar opciones sugeridas
    # =====================================

    def set_options(self, opciones):

        self.context["options"] = list(opciones)

    # =====================================
    # Obtener opciones sugeridas
    # =====================================

    def get_options(self):

        return self.context.get("options", [])

    # =====================================
    # Limpiar opciones
    # =====================================

    def clear_options(self):

        self.context["options"] = []

    # =====================================
    # Completar entidades faltantes
    # =====================================

    def merge(self, entities):

        resultado = deepcopy(entities)

        categorias = resultado.get("categories", [])
        marcas = resultado.get("brands", [])
        productos = resultado.get("products", [])

        # ---------------------------------
        # CASO 1
        # El usuario cambió de categoría.
        # No heredamos marca ni producto.
        # ---------------------------------

        if categorias:

            return resultado

        # ---------------------------------
        # CASO 2
        # El usuario cambió de marca.
        # Heredamos solo la categoría.
        # ---------------------------------

        if marcas:

            if self.context["category"]:

                resultado["categories"] = [
                    self.context["category"]
                ]

            return resultado

        # ---------------------------------
        # CASO 3
        # El usuario seleccionó un producto.
        # Heredamos categoría y marca.
        # ---------------------------------

        if productos:

            if self.context["category"]:

                resultado["categories"] = [
                    self.context["category"]
                ]

            if self.context["brand"]:

                resultado["brands"] = [
                    self.context["brand"]
                ]

            return resultado

        # ---------------------------------
        # CASO 4
        # No se detectó ninguna entidad.
        # Usamos todo el contexto.
        # ---------------------------------

        if self.context["category"]:

            resultado["categories"] = [
                self.context["category"]
            ]

        if self.context["brand"]:

            resultado["brands"] = [
                self.context["brand"]
            ]

        if self.context["product"]:

            resultado["products"] = [
                self.context["product"]
            ]

        return resultado

    # =====================================
    # Construir consulta para el RAG
    # =====================================

    def build_query(self, pregunta):

        partes = []

        pregunta_lower = pregunta.lower()

        # Categoría

        if self.context["category"]:

            categoria = self.context["category"]

            if categoria.lower() not in pregunta_lower:

                partes.append(categoria)

        # Marca

        if self.context["brand"]:

            marca = self.context["brand"]

            if marca.lower() not in pregunta_lower:

                partes.append(marca)

        # Producto

        if self.context["product"]:

            producto = self.context["product"]

            if producto.lower() not in pregunta_lower:

                partes.append(producto)

        partes.append(pregunta)

        consulta = " ".join(partes)

        palabras = consulta.split()

        resultado = []

        for palabra in palabras:

            if palabra.lower() not in [p.lower() for p in resultado]:

                resultado.append(palabra)

        return " ".join(resultado)

    # =====================================
    # Mostrar contexto
    # =====================================

    def debug(self):

        print("\n========== CONTEXTO ==========")

        for clave, valor in self.context.items():

            print(f"{clave}: {valor}")

        print("==============================\n")