from app.embeddings import embeddings

texto = "Hola mundo"

vector = embeddings.embed_query(texto)

print(f"Texto: {texto}")
print(f"Dimensión: {len(vector)}")
print("\nPrimeros 5 valores:")

for valor in vector[:5]:
    print(valor)