import streamlit as st
from crud.usuarios_crud import autenticar_usuario, criar_usuario

def login_screen():
    st.markdown("## 🔐 Login - CustoCerto")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Entrar"):
            user = autenticar_usuario(email, senha)
            if user:
                st.session_state["usuario"] = user
                st.rerun()
            else:
                st.error("Credenciais inválidas")

