from app.utils.text_utils import normalizar_texto


class CatalogAdvisor:

    def __init__(self):

        self.rules = {

            "cara_pequena": {
                "keywords": [
                    "cara pequeña",
                    "rostro pequeño",
                    "cara chica",
                    "rostro chico"
                ],
                "message": (
                    "😊 Para un rostro pequeño te recomendaría estos modelos:\n\n"
                    "• Ray-Ban Meta Skyler\n"
                    "• Ray-Ban Erika\n"
                    "• Ray-Ban Round\n\n"
                    "Estos modelos suelen adaptarse mejor a rostros pequeños.\n\n"
                    "¿Prefieres un modelo clásico, moderno o deportivo?"
                )
            },

            "reloj_regalo": {
                "keywords": [
                    "reloj para regalo",
                    "regalo reloj",
                    "regalar reloj"
                ],
                "message": (
                    "🎁 Si buscas un reloj para regalo, estas son excelentes opciones:\n\n"
                    "• Apple Watch\n"
                    "• Gucci G-Timeless\n"
                    "• Swatch x Omega MoonSwatch\n\n"
                    "¿El regalo es para hombre o mujer?"
                )
            },

            "perfume_elegante": {
                "keywords": [
                    "perfume elegante",
                    "perfume para boda",
                    "perfume formal"
                ],
                "message": (
                    "✨ Si buscas un perfume elegante, te recomendaría:\n\n"
                    "• Creed\n"
                    "• Tom Ford\n"
                    "• Maison Francis Kurkdjian\n\n"
                    "¿Lo buscas para hombre o mujer?"
                )
            }

        }

    def responder(self, pregunta):

        texto = normalizar_texto(pregunta)

        for regla in self.rules.values():

            for keyword in regla["keywords"]:

                if normalizar_texto(keyword) in texto:

                    return regla["message"]

        return None