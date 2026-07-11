from app.services.catalog_service import CatalogService

catalog = CatalogService()

print(catalog.obtener_marcas_normalizadas())