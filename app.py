import streamlit as st
from database import init_db
from  auth import login_screen
from modules import categorias, obras, lancamentos
from crud.obras_crud import listar_obras
from crud.categorias_crud import listar_categorias
from crud.lancamentos_crud import listar_lancamentos

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="CustoCerto | Gestão Inteligente de Obras",
    page_icon="🏗️",
    layout="wide"
)
# =========================
# ESTILO GLOBAL MODERNO
# =========================
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }

    .stButton>button {
        border-radius: 10px;
        height: 40px;
        background-color: #238636;
        color: white;
        border: none;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #2ea043;
    }

    .stTextInput>div>div>input {
        border-radius: 8px;
        height: 40px;
    }

    .stSelectbox>div>div {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# INICIALIZA BANCO
# =========================
init_db()

# =========================
# LOGIN
# =========================
if "usuario" not in st.session_state:
    login_screen()
    st.stop()

usuario = st.session_state["usuario"]
usuario_id = usuario[0]
email = usuario[1]

# =========================
# SIDEBAR SaaS
# =========================
with st.sidebar:
    st.markdown("## 🏗️ CustoCerto")
    st.markdown("---")
    st.markdown(f"👤 **{email}**")

    menu = st.radio(
        "Menu",
        ["Dashboard", "Obras", "Categorias", "Lançamentos"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    if st.button("🚪 Sair"):
        st.session_state.clear()
        st.rerun()

# =========================
# HEADER PRINCIPAL
# =========================
st.markdown("""
    <div style='padding:20px 0'>
        <h1 style='margin-bottom:0'>🏗️ Sistema de Gestão de Obras</h1>
        <p style='color:gray;margin-top:5px'>
            Controle total das suas obras e custos
        </p>
    </div>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
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

# =========================
# OBRAS
# =========================
elif menu == "Obras":
    obras.render(usuario_id)

# =========================
# CATEGORIAS
# =========================
elif menu == "Categorias":
    categorias.render(usuario_id)

# =========================
# LANÇAMENTOS
# =========================
elif menu == "Lançamentos":
    lancamentos.render(usuario_id)