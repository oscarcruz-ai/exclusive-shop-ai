from app.services.product_detector import ProductDetector

detector = ProductDetector()

while True:

    texto = input("Cliente: ")

    if texto.lower() == "salir":
        break

    print()

    print(detector.detectar(texto))

    print()