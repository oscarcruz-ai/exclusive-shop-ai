print("========== INICIO ==========")

from app.services.product_alias_service import ProductAliasService

print("Importación correcta")

service = ProductAliasService()

print("Servicio creado correctamente")

aliases = service.obtener_aliases()

print(f"\nTotal de alias generados: {len(aliases)}\n")

ejemplos = [
    "wayfarer",
    "skyler",
    "headliner",
    "display",
    "dn8",
    "yeezy",
    "zebra",
    "ultra",
]

for alias in ejemplos:

    print("=" * 60)
    print(f"Alias: {alias}")

    if alias in aliases:
        print(f"Producto: {aliases[alias]}")
    else:
        print("No encontrado")

print("\n========== FIN ==========")