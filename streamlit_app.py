# streamlit_app.py
# Interfaz reorganizada + Analytics & ROI

import streamlit as st
from app.agents.sales_agent import SalesAgent
from app.ui.home import render_home
from app.analytics.analytics_store import AnalyticsStore
from app.analytics.roi_store import ROIStore

st.set_page_config(
    page_title="Exclusive Shop AI",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

ANALYTICS_DB = "data/shopagent_analytics.sqlite3"
TENANT_ID = "demo-lumeauren"

analytics = AnalyticsStore(ANALYTICS_DB)
roi = ROIStore(analytics)

st.markdown("""
<style>
[data-testid="stSidebar"]{background:#2b262d;}
.block-container{max-width:1200px;padding-top:.8rem;padding-bottom:1rem;}
h1{text-align:center;font-size:2.8rem !important;margin-bottom:0 !important;}
h3{text-align:center;margin-top:0 !important;margin-bottom:.8rem !important;}
</style>
""", unsafe_allow_html=True)


def consultar_agente(question):
    respuesta = responder_seguimiento(question)

    if respuesta is not None:
        return respuesta

    try:
        return st.session_state.agent.responder(question)
    except Exception:
        return (
            "⚠️ No pude procesar esa consulta en este momento. "
            "Intenta escribir el nombre del producto, una marca o tu pregunta de nuevo."
        )


def es_consulta_seguimiento(texto):
    texto = texto.casefold()

    return any(
        expresion in texto
        for expresion in (
            "seguimiento",
            "tracking",
            "rastrear",
            "rastreame",
            "donde esta mi pedido",
            "dónde está mi pedido",
            "estado de mi pedido",
        )
    )


def extraer_numero_pedido(texto):
    import re

    coincidencia = re.search(r"(?:pedido|orden)\s*#?\s*(\d+)", texto, re.IGNORECASE)

    if not coincidencia:
        coincidencia = re.search(r"#(\d+)", texto)

    return int(coincidencia.group(1)) if coincidencia else None


def es_email_valido(texto):
    import re

    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", texto.strip()))


def responder_seguimiento(prompt):
    """Gestiona el flujo de seguimiento dentro de la sesión del cliente."""
    estado = st.session_state.get("tracking_estado")

    if estado == "numero_pedido":
        order_id = extraer_numero_pedido(prompt)

        if not order_id:
            return "Por favor, indícame el número de pedido. Ejemplo: **Pedido #42916**."

        st.session_state.tracking_order_id = order_id
        st.session_state.tracking_estado = "email"
        return "Ahora indícame el correo que usaste al realizar la compra."

    if estado == "email":
        if not es_email_valido(prompt):
            return "Ingresa el correo usado en la compra para verificar el pedido."

        order_id = st.session_state.get("tracking_order_id")
        st.session_state.tracking_estado = None
        st.session_state.tracking_order_id = None

        resultado = st.session_state.agent.consultar_seguimiento_autorizado(
            order_id,
            prompt,
        )

        if not resultado.get("empresa"):
            return resultado["mensaje"]

        detalle_orden = ""
        if resultado.get("numero_orden"):
            detalle_orden = f"\n🧾 N.º de orden: `{resultado['numero_orden']}`"

        return (
            f"📦 **Pedido #{resultado['order_id']}**\n\n"
            f"🚚 {resultado['empresa']}\n"
            f"🔎 Código de seguimiento: `{resultado['codigo']}`"
            f"{detalle_orden}\n\n"
            f"🔗 [Rastrear en el portal oficial]({resultado['url']})\n\n"
            f"{resultado['mensaje']}"
        )

    if not es_consulta_seguimiento(prompt):
        return None

    order_id = extraer_numero_pedido(prompt)

    if not order_id:
        st.session_state.tracking_estado = "numero_pedido"
        return "Claro. Indícame el número de tu pedido para buscar el seguimiento."

    st.session_state.tracking_order_id = order_id
    st.session_state.tracking_estado = "email"
    return "Para proteger tu información, indícame el correo usado en la compra."


st.session_state.setdefault("messages", [])
st.session_state.setdefault("quick_question", None)
st.session_state.setdefault("selected_button", None)

if "agent" not in st.session_state:
    st.session_state.agent = SalesAgent()


with st.sidebar:
    st.image(
        "assets/logo-exclusive.png",
        width=280
    )

    st.link_button(
        "🛒 Visitar Exclusive Shop",
        "https://www.exclusiveshopperu.com",
        use_container_width=True
    )

    st.markdown("---")

    st.markdown("### 📋 Asesor Premium")
    st.markdown("*Especializado en:*")

    st.markdown("""
- 👓 **Ray-Ban Meta**
- 📱 **Apple**
- 🕶️ **Lentes exclusivos**
- 👟 **Zapatillas**
- ⌚ **Relojes**
- 👕 **Streetwear**
""")

    st.markdown("---")

    vista = st.radio(
        "Sección",
        ["🛍️ ShopAgent", "📊 Analytics & ROI"]
    )

    st.markdown("---")
    st.caption("© 2026 Exclusive Shop")


# ============================================================
# DASHBOARD ANALYTICS
# ============================================================

if vista == "📊 Analytics & ROI":

    st.title("📊 Analytics & ROI")
    st.subheader("Panel de rendimiento de ShopAgent")

    resumen = analytics.summary(TENANT_ID, 30)

    st.caption(
        "Demo tenant: demo-lumeauren · Últimos 30 días"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Conversaciones",
        f"{resumen['conversations']:,}"
    )

    col2.metric(
        "Recomendaciones",
        f"{resumen['recommendations']:,}"
    )

    col3.metric(
        "Intenciones de checkout",
        f"{resumen['checkout_intents']:,}"
    )

    col4.metric(
        "Compras",
        f"{resumen['purchases']:,}"
    )

    st.divider()

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "Ingresos",
        f"S/ {resumen['revenue']:,.2f}"
    )

    col6.metric(
        "Tasa de checkout",
        f"{resumen['checkout_rate']:.2f}%"
    )

    col7.metric(
        "Conversión a compra",
        f"{resumen['purchase_rate']:.2f}%"
    )

    st.divider()

    st.subheader("📈 Embudo de conversión")

    funnel_col1, funnel_col2, funnel_col3 = st.columns(3)

    funnel_col1.metric(
        "Conversaciones",
        f"{resumen['conversations']:,}"
    )

    funnel_col2.metric(
        "Checkout",
        f"{resumen['checkout_intents']:,}"
    )

    funnel_col3.metric(
        "Compras",
        f"{resumen['purchases']:,}"
    )


# ============================================================
# SHOPAGENT
# ============================================================

else:

    st.title("Exclusive Shop AI")
    st.subheader("Tu asesor inteligente de compras")
    st.info("👋 ¿Qué producto estás buscando hoy?")

    consulta = render_home()

    if consulta:
        st.session_state.quick_question = consulta

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    prompt = st.chat_input("Escribe tu consulta...")

    if st.session_state.quick_question and not prompt:
        prompt = st.session_state.quick_question
        st.session_state.quick_question = None

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Consultando al asesor inteligente..."
            ):
                respuesta = consultar_agente(prompt)

            st.markdown(respuesta)

            st.session_state.messages.append({
                "role": "assistant",
                "content": respuesta
            })

        st.session_state.selected_button = None
        st.rerun()