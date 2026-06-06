import streamlit as st
from database import init_db
from auth import login_screen

# IMPORTAÇÃO DOS MÓDULOS DE TELAS (Adicionado fornecedores)
from modules import categorias, obras, lancamentos, fornecedores

# IMPORTAÇÃO DOS CRUDS (Adicionado listar_fornecedores)
from crud.obras_crud import listar_obras
from crud.categorias_crud import listar_categorias
from crud.lancamentos_crud import listar_lancamentos
from crud.fornecedor_crud import listar_fornecedores

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
# SISTEMA DE NAVEGAÇÃO PERSISTENTE
# =========================
opcoes_menu = ["Dashboard", "Obras", "Categorias", "Lançamentos", "Fornecedores"]

if "menu_atual" not in st.session_state:
    st.session_state["menu_atual"] = "Dashboard"

id_atual = opcoes_menu.index(st.session_state["menu_atual"])

# =========================
# SIDEBAR SaaS
# =========================
with st.sidebar:
    st.markdown("## 🏗️ CustoCerto")
    st.markdown("---")
    st.markdown(f"👤 **{email}**")

    menu = st.radio(
        "Menu",
        opcoes_menu,
        index=id_atual,
        label_visibility="collapsed"
    )
    # Atualiza o estado da sessão com o clique atual
    st.session_state["menu_atual"] = menu

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
if st.session_state["menu_atual"] == "Dashboard":

    df_obras = listar_obras(usuario_id)
    df_cat = listar_categorias(usuario_id)
    df_lanc = listar_lancamentos(usuario_id)
    df_forn = listar_fornecedores(usuario_id) # Buscando dados de fornecedores

    # Mudado para 4 colunas para incluir os Fornecedores nas métricas
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏗️ Obras", len(df_obras))
    col2.metric("🏢 Fornecedores", len(df_forn))
    col3.metric("📁 Categorias", len(df_cat))
    col4.metric("💰 Lançamentos", len(df_lanc))

    st.divider()

    st.subheader("📊 Últimos Lançamentos")

    if not df_lanc.empty:
        st.dataframe(df_lanc, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum lançamento ainda.")

# =========================
# OBRAS
# =========================
elif st.session_state["menu_atual"] == "Obras":
    obras.render(usuario_id)

# =========================
# CATEGORIAS
# =========================
elif st.session_state["menu_atual"] == "Categorias":
    categorias.render(usuario_id)

# =========================
# LANÇAMENTOS
# =========================
elif st.session_state["menu_atual"] == "Lançamentos":
    lancamentos.render(usuario_id)

# =========================
# FORNECEDORES (Adicionado bloco que faltava)
# =========================
elif st.session_state["menu_atual"] == "Fornecedores":
    fornecedores.render(usuario_id)