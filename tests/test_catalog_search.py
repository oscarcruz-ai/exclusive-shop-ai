from app.services.catalog_service import CatalogService

catalog = CatalogService()

print("=" * 50)
print("Buscar producto: Skyler")
print("=" * 50)

print(
    catalog.buscar_producto("Skyler")
)

print("\n")

print("=" * 50)
print("Productos Ray-Ban")
print("=" * 50)

print(
    catalog.obtener_productos_por_marca("Ray-Ban")
)

print("\n")

print("=" * 50)
print("Productos Skincare")
print("=" * 50)

print(
    catalog.obtener_productos_por_categoria("Skincare")
)