import streamlit as st
from crud.categorias_crud import criar_categoria, listar_categorias


def render(usuario_id):

    st.subheader("📁 Categorias")

    # ==========================================
    # BOTÃO PARA ABRIR MODAL
    # ==========================================
    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("➕ Nova Categoria"):
            abrir_modal_categoria(usuario_id)

    # ==========================================
    # LISTAGEM
    # ==========================================
    df = listar_categorias(usuario_id)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhuma categoria cadastrada.")


# ==========================================
# MODAL
# ==========================================
@st.dialog("Nova Categoria")
def abrir_modal_categoria(usuario_id):

    descricao = st.text_input("Descrição da categoria")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Salvar", use_container_width=True):
            if descricao.strip() == "":
                st.warning("Informe uma descrição.")
            else:
                criar_categoria(usuario_id, descricao)
                st.success("Categoria criada com sucesso!")
                st.rerun()

    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()