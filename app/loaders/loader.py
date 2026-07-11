from app.loaders.csv_loader import cargar_catalogo
from app.loaders.pdf_loader import cargar_pdfs


def cargar_documentos(ruta_csv, carpeta_pdf):
    """
    Carga catálogo y PDFs y devuelve una sola lista de documentos.
    """

    documentos = []

    documentos.extend(cargar_catalogo(ruta_csv))
    documentos.extend(cargar_pdfs(carpeta_pdf))

    return documentos