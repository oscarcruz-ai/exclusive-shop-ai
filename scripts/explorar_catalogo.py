from app.services.catalog_service import CatalogService

catalog = CatalogService()

productos = catalog.obtener_nombres_productos()

print(f"\nTotal de productos: {len(productos)}\n")

print("=" * 80)

for i, producto in enumerate(productos[:200], start=1):
    print(f"{i:03d}. {producto}")