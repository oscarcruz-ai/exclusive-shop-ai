import streamlit as st


def load_styles():

    st.markdown("""
    <style>

    .block-container{
        padding-top:2rem;
    }

    [data-testid="stSidebar"] .block-container{
        padding-top:0.5rem;
    }

    div.stButton > button{
        width:100%;
        border-radius:10px;
        height:55px;
        font-weight:600;
        border:1px solid #d9d9d9;
    }

    div.stButton > button:hover{
        border:1px solid #4F8BF9;
    }

    </style>
    """, unsafe_allow_html=True)