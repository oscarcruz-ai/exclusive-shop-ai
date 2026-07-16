from app.utils.text_utils import normalizar_texto


class IntentDetector:

    PALABRAS_INFORMACION = [
        "diferencia",
        "comparar",
        "comparación",
        "vs",
        "versus",
        "mejor",
        "recomiendas",
        "recomendar",
        "cómo funciona",
        "como funciona",
        "vale la pena",
        "opinión",
        "opinion",
        "qué cambia",
        "que cambia"
    ]

    def detectar(self, pregunta):

        texto = normalizar_texto(pregunta)

        for palabra in self.PALABRAS_INFORMACION:

            if palabra in texto:
                return "information"

        return "catalog"