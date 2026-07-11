from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def cargar_pdfs(carpeta_pdf):
    """
    Carga todos los PDFs de una carpeta y devuelve una lista de Document.
    """

    documentos = []

    carpeta = Path(carpeta_pdf)

    for archivo in carpeta.glob("*.pdf"):

        loader = PyPDFLoader(str(archivo))

        paginas = loader.load()

        for pagina in paginas:

            pagina.metadata["tipo"] = "documento"
            pagina.metadata["archivo"] = archivo.name

        documentos.extend(paginas)

    return documentos