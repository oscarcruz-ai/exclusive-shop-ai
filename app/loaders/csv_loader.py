import pandas as pd

from langchain_core.documents import Document


def cargar_catalogo(ruta_csv):
    """
    Lee el catálogo y devuelve una lista de Document.
    """

    df = pd.read_csv(ruta_csv)

    documentos = []

    for _, fila in df.iterrows():

        contenido = "\n".join(
            f"{col}: {fila[col]}"
            for col in df.columns
        )

        documentos.append(
            Document(
                page_content=contenido,
                metadata={
                    "tipo": "producto"
                }
            )
        )

    return documentos