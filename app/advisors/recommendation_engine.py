from app.advisors.consultation_rules import CONSULTATION_RULES


class RecommendationEngine:

    def obtener_pregunta(self, texto):

        texto = texto.lower()

        for _, datos in CONSULTATION_RULES.items():

            for keyword in datos["keywords"]:

                if keyword.lower() in texto:

                    return datos["questions"][0]

        return None