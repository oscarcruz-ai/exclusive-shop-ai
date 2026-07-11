class IntentClassifier:

    def detectar(self, pregunta):

        texto = pregunta.lower()

        if any(p in texto for p in [
            "recomienda",
            "recomendación",
            "cuál me conviene",
            "cuál elegir"
        ]):
            return "recommendation"

        if any(p in texto for p in [
            "diferencia",
            "comparar",
            "vs"
        ]):
            return "comparison"

        if any(p in texto for p in [
            "precio",
            "cuesta",
            "vale"
        ]):
            return "price"

        if any(p in texto for p in [
            "stock",
            "disponible",
            "tienen"
        ]):
            return "stock"

        return "general"