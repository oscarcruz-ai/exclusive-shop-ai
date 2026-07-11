from app.services.catalog_service import CatalogService

catalog = CatalogService()

while True:

    texto = input("Cliente: ")

    if texto.lower() == "salir":
        break

    print()

    print(catalog.detectar_marcas(texto))

    print()