from app.agents.sales_agent import SalesAgent

agent = SalesAgent()

print("Exclusive Shop Sales Agent\n")

while True:

    pregunta = input("Cliente: ")

    if pregunta.lower() == "salir":
        break

    respuesta = agent.responder(pregunta)

    print("\nAsesor:", respuesta)
    print()