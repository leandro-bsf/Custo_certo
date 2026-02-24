import streamlit as st
from pages import categorias, obras, lancamentos
from crud.obras_crud import listar_obras
from crud.categorias_crud import listar_categorias
from crud.lancamentos_crud import listar_lancamentos


def render():
    usuario = st.session_state["usuario"]
    usuario_id = usuario[0]
    email = usuario[1]

    # ==========================================
    # CONFIGURAÇÃO DA PÁGINA
    # ==========================================
    st.set_page_config(layout="wide")

    # ==========================================
    # CSS MODERNO
    # ==========================================
    st.markdown("""
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 40px;
            background-color: #111827;
            border-radius: 12px;
            margin-bottom: 30px;
        }

        .nav-left {
            display: flex;
            gap: 30px;
            align-items: center;
        }

        .logo {
            font-size: 22px;
            font-weight: bold;
            color: white;
        }

        .user-email {
            color: #9CA3AF;
            font-size: 14px;
        }

        .content-box {
            padding: 30px;
            background-color: #1F2937;
            border-radius: 15px;
        }

        div[data-testid="metric-container"] {
            background-color: #1F2937;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }

        </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # NAVBAR SUPERIOR
    # ==========================================
    col_logo, col_menu, col_user, col_logout = st.columns([2, 4, 2, 1])

    with col_logo:
        st.markdown("### 📸 Photo Love")

    with col_menu:
        menu = st.radio(
            "",
            ["Dashboard", "Obras", "Categorias", "Lançamentos"],
            horizontal=True,
            label_visibility="collapsed"
        )

    with col_user:
        st.markdown(f"👤 **{email}**")

    with col_logout:
        if st.button("🚪"):
            st.session_state.clear()
            st.rerun()

    st.divider()

    # ==========================================
    # HEADER PRINCIPAL
    # ==========================================
    st.markdown("""
        <div style='margin-bottom:30px'>
            <h1 style='margin-bottom:5px'>🏗️ Sistema de Gestão de Obras</h1>
            <p style='color:gray;margin-top:0'>
                Controle total das suas obras e custos
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # DASHBOARD
    # ==========================================
    if menu == "Dashboard":

        df_obras = listar_obras(usuario_id)
        df_cat = listar_categorias(usuario_id)
        df_lanc = listar_lancamentos(usuario_id)

        col1, col2, col3 = st.columns(3)

        col1.metric("🏗️ Obras", len(df_obras))
        col2.metric("📁 Categorias", len(df_cat))
        col3.metric("💰 Lançamentos", len(df_lanc))

        st.divider()

        st.subheader("📊 Últimos Lançamentos")
        if not df_lanc.empty:
            st.dataframe(df_lanc, use_container_width=True)
        else:
            st.info("Nenhum lançamento ainda.")

    # ==========================================
    # OUTRAS TELAS
    # ==========================================
    elif menu == "Obras":
        obras.render(usuario_id)

    elif menu == "Categorias":
        categorias.render(usuario_id)

    elif menu == "Lançamentos":
        lancamentos.render(usuario_id)