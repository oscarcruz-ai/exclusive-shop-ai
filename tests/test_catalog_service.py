from app.services.catalog_service import CatalogService

catalog = CatalogService()

print("\nMarcas:\n")

for marca in catalog.obtener_marcas():
    print("-", marca)

print("\nCategorías limpias:\n")

for categoria in catalog.obtener_categorias_limpias():
    print("-", categoria)