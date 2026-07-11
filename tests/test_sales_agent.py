from app.agents.sales_agent import SalesAgent

agent = SalesAgent()

print("=" * 55)
print("      Exclusive Shop AI")
print(" Asesor Premium de Productos Exclusivos")
print("=" * 55)
print("Escribe 'salir' para terminar.\n")

while True:

    pregunta = input("Cliente: ")

    if pregunta.lower() == "salir":
        break

    respuesta = agent.responder(pregunta)

    print()
    print("Asesor:", respuesta)
    print()