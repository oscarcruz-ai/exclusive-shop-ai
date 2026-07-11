from app.llm import llm

respuesta = llm.invoke("Di únicamente: Hola Oscar")

print(respuesta.content)