import streamlit as st


def init_chat():

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content":
                    "👋 **¡Bienvenido a Exclusive Shop!**\n\n"
                    "Soy tu asesor premium especializado en productos exclusivos.\n\n"
                    "¿Qué producto estás buscando hoy?"
            }
        ]


def show_chat():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def add_user_message(texto):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": texto
        }
    )

    with st.chat_message("user"):
        st.markdown(texto)


def add_assistant_message(texto):

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": texto
        }
    )

    with st.chat_message("assistant"):
        st.markdown(texto)


def process_message(agent, texto):

    add_user_message(texto)

    with st.spinner("🔍 Buscando la mejor opción para ti..."):

        respuesta = agent.responder(texto)

    add_assistant_message(respuesta)


def chat_input():

    return st.chat_input(
        "Escribe tu consulta...",
        key="main_chat"
    )