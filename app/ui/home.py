import streamlit as st


def boton(texto, consulta, key):
    """
    Renderiza un botón y mantiene el estado del último seleccionado.
    """

    seleccionado = (
        st.session_state.selected_button == key
    )

    etiqueta = (
        f"✅ {texto}"
        if seleccionado
        else texto
    )

    if st.button(
        etiqueta,
        key=key,
        use_container_width=True
    ):
        st.session_state.selected_button = key
        return consulta

    return None


def render_home():

    consulta = None

    izquierda, derecha = st.columns(
        2,
        gap="large"
    )

    # =====================================
    # Categorías
    # =====================================

    with izquierda:

        st.markdown("### 🔍 Explorar categorías")

        c1, c2 = st.columns(2)

        with c1:

            if resultado := boton(
                "👓 Ray-Ban Meta",
                "Ray-Ban Meta",
                "btn_rayban"
            ):
                consulta = resultado

            if resultado := boton(
                "👟 Zapatillas",
                "Zapatillas",
                "btn_zapatillas"
            ):
                consulta = resultado

        with c2:

            if resultado := boton(
                "📱 Apple",
                "Apple",
                "btn_apple"
            ):
                consulta = resultado

            if resultado := boton(
                "⌚ Relojes",
                "Relojes",
                "btn_relojes"
            ):
                consulta = resultado

    # =====================================
    # Preguntas frecuentes
    # =====================================

    with derecha:

        st.markdown("### ❓ Preguntas frecuentes")

        c3, c4 = st.columns(2)

        with c3:

            if resultado := boton(
                "🚚 Envíos",
                "Envíos",
                "btn_envios"
            ):
                consulta = resultado

            if resultado := boton(
                "🛡️ Garantía",
                "Garantía",
                "btn_garantia"
            ):
                consulta = resultado

        with c4:

            if resultado := boton(
                "💳 Pagos",
                "Métodos de pago",
                "btn_pagos"
            ):
                consulta = resultado

            if resultado := boton(
                "📦 Originalidad",
                "¿Es original?",
                "btn_originalidad"
            ):
                consulta = resultado

    return consulta