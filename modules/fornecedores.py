import streamlit as st

from crud.fornecedor_crud import (
    criar_fornecedor,
    listar_fornecedores
)


# =====================================================
# RENDER PRINCIPAL
# =====================================================
def render(usuario_id: int):

    st.subheader("🏢 Fornecedores")

    col1, col2 = st.columns([6, 1])

    with col2:
        # Criamos uma chave no session_state para controlar se o modal deve abrir
        if st.button("➕ Novo Fornecedor"):
            abrir_modal_fornecedor(usuario_id)

    st.divider()

    st.subheader("📋 Fornecedores Cadastrados")

    df = listar_fornecedores(usuario_id)

    if df.empty:
        st.info("Nenhum fornecedor cadastrado.")
        return

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# MODAL NOVO FORNECEDOR
# =====================================================
@st.dialog("Cadastrar Fornecedor")
def abrir_modal_fornecedor(usuario_id):

    with st.form("form_fornecedor", clear_on_submit=True): # clear_on_submit ajuda a limpar os campos

        nome = st.text_input("Nome do Fornecedor")

        col1, col2 = st.columns(2)
        cnpj = col1.text_input("CNPJ")
        telefone = col2.text_input("Telefone")

        col3, col4 = st.columns(2)
        email = col3.text_input("E-mail")
        cidade = col4.text_input("Cidade")

        observacao = st.text_area("Observação", height=100)

        col_btn1, col_btn2 = st.columns(2)

        salvar = col_btn1.form_submit_button(
            "💾 Salvar",
            use_container_width=True
        )
        
        # Transformamos o botão cancelar em um submit que apenas fecha o modal visualmente
        cancelar = col_btn2.form_submit_button(
            "❌ Cancelar",
            use_container_width=True
        )

        if salvar:
            if not nome.strip():
                st.warning("Informe o nome do fornecedor.")
                return

            criar_fornecedor(
                usuario_id=usuario_id,
                nome=nome.strip(),
                cnpj=cnpj.strip(),
                telefone=telefone.strip(),
                email=email.strip(),
                cidade=cidade.strip(),
                observacao=observacao.strip()
            )

            st.success("Fornecedor cadastrado com sucesso!")
            # Em vez de st.rerun(), usamos o rerun específico para atualizar a tabela de trás do modal
            st.rerun() 

        if cancelar:
            # Força o fechamento do modal sem resetar o menu global
            st.rerun()