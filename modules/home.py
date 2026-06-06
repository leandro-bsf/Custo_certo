import streamlit as st

from pages import (
    obras,
    categorias,
    lancamentos,
    fornecedores
)

from crud.obras_crud import listar_obras
from crud.categorias_crud import listar_categorias  # Verifique se no seu arquivo está categorias_crud
from crud.lancamentos_crud import listar_lancamentos
from crud.fornecedor_crud import listar_fornecedores


def render():

    usuario = st.session_state["usuario"]

    usuario_id = usuario[0]
    email = usuario[1]

    # =====================================================
    # CONFIGURAÇÃO
    # =====================================================
    st.set_page_config(
        page_title="Gestão de Obras",
        page_icon="🏗️",
        layout="wide"
    )

    # =====================================================
    # CSS
    # =====================================================
    st.markdown("""
    <style>
    .main-title{
        margin-bottom:0;
    }
    div[data-testid="metric-container"]{
        background:#1F2937;
        padding:20px;
        border-radius:15px;
        border:1px solid #374151;
    }
    </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # TOPO & SISTEMA DE NAVEGAÇÃO PERSISTENTE
    # =====================================================
    col_logo, col_menu, col_user, col_logout = st.columns(
        [2, 5, 2, 1]
    )

    with col_logo:
        st.markdown("## 🏗️ Gestão Obras")

    # Lista de opções do menu
    opcoes_menu = ["Dashboard", "Obras", "Fornecedores", "Categorias", "Lançamentos"]

    # Inicializa o estado do menu se ele não existir
    if "menu_atual" not in st.session_state:
        st.session_state["menu_atual"] = "Dashboard"

    # Descobre o índice da tela atual para manter o botão marcado
    id_atual = opcoes_menu.index(st.session_state["menu_atual"])

    with col_menu:
        menu = st.radio(
            "",
            opcoes_menu,
            index=id_atual, # Define o botão ativo dinamicamente
            horizontal=True,
            label_visibility="collapsed"
        )
        # Atualiza a sessão com a nova escolha do usuário
        st.session_state["menu_atual"] = menu

    with col_user:
        st.markdown(f"👤 **{email}**")

    with col_logout:
        if st.button("🚪 Sair"):
            st.session_state.clear()
            st.rerun()

    st.divider()

    # =====================================================
    # HEADER
    # =====================================================
    st.markdown("""
    <div style="margin-bottom:20px">
        <h1>🏗️ Sistema de Gestão de Obras</h1>
        <p style="color:gray">
            Controle completo de obras, custos e fornecedores.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # RENDEREZACAO DAS TELAS (Baseado na sessão persistente)
    # =====================================================
    if st.session_state["menu_atual"] == "Dashboard":

        df_obras = listar_obras(usuario_id)
        df_cat = listar_categorias(usuario_id)
        df_lanc = listar_lancamentos(usuario_id)
        df_forn = listar_fornecedores(usuario_id)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🏗️ Obras", len(df_obras))

        with col2:
            st.metric("🏢 Fornecedores", len(df_forn))

        with col3:
            st.metric("📁 Categorias", len(df_cat))

        with col4:
            st.metric("💰 Lançamentos", len(df_lanc))

        st.divider()

        st.subheader("📋 Últimos Lançamentos")

        if not df_lanc.empty:
            st.dataframe(
                df_lanc,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhum lançamento encontrado.")

    elif st.session_state["menu_atual"] == "Obras":
        obras.render(usuario_id)

    elif st.session_state["menu_atual"] == "Fornecedores":
        fornecedores.render(usuario_id)

    elif st.session_state["menu_atual"] == "Categorias":
        categorias.render(usuario_id)

    elif st.session_state["menu_atual"] == "Lançamentos":
        lancamentos.render(usuario_id)