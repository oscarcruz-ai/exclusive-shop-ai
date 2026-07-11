from app.advisors.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()

while True:

    texto = input("Cliente: ")

    if texto == "salir":
        break

    pregunta = engine.obtener_pregunta(texto)

    print()

    print(pregunta)

    print()