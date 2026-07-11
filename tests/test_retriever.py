from app.retriever import retriever

consulta = "Ray-Ban Meta"

documentos = retriever.invoke(consulta)

print(f"Resultados encontrados: {len(documentos)}")

for i, doc in enumerate(documentos, start=1):

    print("\n===========================")
    print(f"Documento {i}")
    print("===========================\n")

    print(doc.page_content[:700])