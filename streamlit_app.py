import streamlit as st
from app.agents.sales_agent import SalesAgent
from app.ui.home import render_home

# ===================================
# Configuración
# ===================================

st.set_page_config(
    page_title="Exclusive Shop AI | Premium Shopping Assistant",
    page_icon="🛍️",
    layout="wide"
)

# ===================================
# Estilos Personalizados
# ===================================

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background-color:#2b262d;
}

.block-container{
    max-width:1200px;
    padding-top:2rem;
}

div.stButton > button{
    width:100%;
    height:50px;
    border-radius:10px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# Inicialización de Estado
# ===================================

if "agent" not in st.session_state:
    st.session_state.agent = SalesAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None

if "selected_button" not in st.session_state:
    st.session_state.selected_button = None

# ===================================
# Sidebar
# ===================================

with st.sidebar:

    st.markdown("## 📋 Asesor Premium")

    st.markdown("Especializado en:")

    st.markdown("""
- 👓 Ray-Ban Meta
- 🕶️ Lentes exclusivos
- 📱 Productos Apple
- 👟 Zapatillas exclusivas
- ⌚ Relojes
- 👕 Streetwear
""")

# ===================================
# Encabezado
# ===================================

st.markdown(
    "<h1 style='text-align:center;'>Exclusive Shop AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align:center;'>Tu asesor inteligente de compras</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Encuentra productos exclusivos, compara modelos y resuelve tus dudas.</p>",
    unsafe_allow_html=True
)

# ===================================
# Botones Home
# ===================================

consulta = render_home()

if consulta:
    st.session_state.quick_question = consulta

# ===================================
# Historial
# ===================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ===================================
# Chat Input
# ===================================

prompt = st.chat_input("Escribe tu consulta...")

# ===================================
# Consulta rápida
# ===================================

if st.session_state.quick_question and not prompt:

    prompt = st.session_state.quick_question

    st.session_state.quick_question = None

# ===================================
# Procesar consulta
# ===================================

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Buscando..."):

            respuesta = st.session_state.agent.responder(prompt)

        st.markdown(respuesta)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": respuesta
            }
        )

    # Limpiar el botón seleccionado
    st.session_state.selected_button = None

    st.rerun()