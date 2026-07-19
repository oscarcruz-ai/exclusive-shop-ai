# streamlit_app.py
# Interfaz reorganizada

import requests
import streamlit as st
from app.ui.home import render_home

API_URL = "https://api.exclusiveshopperu.com/ask"

st.set_page_config(
    page_title="Exclusive Shop AI",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebar"]{background:#2b262d;}
.block-container{max-width:1200px;padding-top:.8rem;padding-bottom:1rem;}
h1{text-align:center;font-size:2.8rem !important;margin-bottom:0 !important;}
h3{text-align:center;margin-top:0 !important;margin-bottom:.8rem !important;}
</style>
""", unsafe_allow_html=True)

def consultar_api(question):
    try:
        r=requests.post(API_URL,json={"question":question},timeout=120)
        r.raise_for_status()
        return r.json().get("answer","No se recibió respuesta.")
    except requests.exceptions.Timeout:
        return "⏳ El asistente tardó demasiado en responder."
    except requests.exceptions.ConnectionError:
        return "❌ No fue posible conectar con Exclusive Shop AI."
    except Exception as e:
        return f"❌ Error:\n\n{e}"

st.session_state.setdefault("messages",[])
st.session_state.setdefault("quick_question",None)
st.session_state.setdefault("selected_button",None)

with st.sidebar:
    st.image("assets/logo-exclusive.png", 
             width=280
    )
    st.link_button(
        "🛒 Visitar Exclusive Shop",
        "https://www.exclusiveshopperu.com",
        use_container_width=True
    )
    st.markdown("---")
    st.markdown("### 🛍️ Especializado en")
    
    st.markdown("""
- 👓 **Ray-Ban Meta**
- 📱 **Apple**
- 🕶️ **Lentes exclusivos**
- 👟 **Zapatillas**
- ⌚ **Relojes**
- 👕 **Streetwear**
""")
    st.markdown("---")
    st.caption("© 2026 Exclusive Shop")

st.title("Exclusive Shop AI")
st.subheader("Tu asesor inteligente de compras")
st.info("👋 ¿Qué producto estás buscando hoy?")

consulta=render_home()
if consulta:
    st.session_state.quick_question=consulta

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt=st.chat_input("Escribe tu consulta...")

if st.session_state.quick_question and not prompt:
    prompt=st.session_state.quick_question
    st.session_state.quick_question=None

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("🤖 Consultando al asesor inteligente..."):
            respuesta=consultar_api(prompt)
        st.markdown(respuesta)
        st.session_state.messages.append({"role":"assistant","content":respuesta})
    st.session_state.selected_button=None
    st.rerun()