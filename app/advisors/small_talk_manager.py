class SmallTalkManager:

    def responder(self, pregunta):

        texto = pregunta.lower().strip()

        # ======================
        # SALUDOS
        # ======================

        saludos = {
            "hola",
            "buenas",
            "buenos dias",
            "buen día",
            "buen dia",
            "buenas tardes",
            "buenas noches",
            "que tal",
            "hey",
            "hi",
            "holi"
        }

        if texto in saludos:
            return (
                "👋 ¡Hola! Bienvenido a Exclusive Shop.\n\n"
                "Estoy aquí para ayudarte a encontrar el producto ideal.\n\n"
                "¿Qué estás buscando hoy?"
            )

        # ======================
        # DESPEDIDAS
        # ======================

        despedidas = {
            "chau",
            "adios",
            "adiós",
            "hasta luego",
            "nos vemos",
            "bye"
        }

        if texto in despedidas:
            return (
                "👋 ¡Gracias por visitar Exclusive Shop!\n\n"
                "Cuando necesites ayuda para encontrar un producto exclusivo, aquí estaré."
            )

        # ======================
        # AGRADECIMIENTOS
        # ======================

        agradecimientos = {
            "gracias",
            "muchas gracias",
            "perfecto",
            "excelente",
            "ok gracias"
        }

        if texto in agradecimientos:
            return (
                "😊 ¡Con mucho gusto!\n\n"
                "Si necesitas ayuda con otro producto, aquí estaré."
            )

        # ======================
        # OFERTAS
        # ======================

        ofertas = {
            "ofertas",
            "descuentos",
            "promociones",
            "promo"
        }

        if texto in ofertas:
            return (
                "🏷️ Tenemos novedades y promociones que pueden variar según el producto.\n\n"
                "¿Qué producto o marca te interesa?"
            )

        # ======================
        # MUY CARO
        # ======================

        objeciones = {
            "muy caro",
            "esta caro",
            "está caro",
            "caro",
            "muy costoso"
        }

        if texto in objeciones:
            return (
                "💬 Entiendo.\n\n"
                "¿Qué presupuesto tienes aproximadamente?\n\n"
                "Así puedo ayudarte a encontrar una mejor opción."
            )

        # ======================
        # ORIGINAL
        # ======================

        originales = {
            "es original",
            "son originales",
            "original",
            "originales"
        }

        if texto in originales:
            return (
                "✅ Sí. Todos nuestros productos son originales y se comercializan a pedido."
            )

        # ======================
        # GARANTÍA
        # ======================

        garantia = {
            "garantia",
            "garantía",
            "tiene garantia",
            "tiene garantía"
        }

        if texto in garantia:
            return (
                "🛡️ La garantía depende del tipo de producto y del fabricante.\n\n"
                "¿Sobre qué producto deseas consultar?"
            )

        # ======================
        # ENVÍOS
        # ======================

        envios = {
            "envio",
            "envío",
            "envios",
            "envíos"
        }

        if texto in envios:
            return (
                "🚚 Realizamos envíos a todo el Perú.\n\n"
                "¿Qué producto deseas comprar?"
            )

        return None