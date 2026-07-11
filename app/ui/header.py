import streamlit as st


def render_header():

    st.markdown("""
    <h1 style="text-align:center;">
        Exclusive Shop AI
    </h1>

    <h3 style="text-align:center;font-weight:400;">
        Tu asesor inteligente de compras
    </h3>

    <p style="text-align:center;font-size:18px;">
        Encuentra productos, compara modelos y resuelve tus dudas
        sobre envíos, pagos y garantía.
    </p>
    """, unsafe_allow_html=True)

    st.divider()