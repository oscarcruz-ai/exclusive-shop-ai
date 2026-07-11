from app.chatbot import ExclusiveShopBot

bot = ExclusiveShopBot()

print("Exclusive Shop AI")
print("Escribe 'salir' para terminar.\n")

while True:

    pregunta = input("Tú: ")

    if pregunta.lower() == "salir":
        break

    respuesta = bot.responder(pregunta)

    print("\nBot:", respuesta)
    print()