from datetime import datetime

from app.prompts.system_prompt import SYSTEM_PROMPT
from app.prompts.sales_prompt import SALES_PROMPT


def construir_prompt(
    contexto,
    pregunta,
    historial=""
):
    fecha = datetime.now().strftime("%d/%m/%Y")

    return f"""
{SYSTEM_PROMPT}

{SALES_PROMPT}

Fecha actual:
{fecha}

Historial de conversación:
{historial}

Contexto:
{contexto}

Pregunta del cliente:
{pregunta}
"""