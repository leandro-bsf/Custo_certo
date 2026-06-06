from crud.fornecedor_crud import listar_fornecedores
import streamlit as st
import plotly.express as px
from crud.lancamentos_crud import (
    criar_lancamento,
    listar_lancamentos,
    resumo_por_categoria
)
from crud.obras_crud import listar_obras
from crud.categorias_crud import listar_categorias


# =====================================================
# RENDER PRINCIPAL
# =====================================================
def render(usuario_id: int):

    st.subheader("💰 Lançamentos")

    df_obras = listar_obras(usuario_id)
    df_cat = listar_categorias(usuario_id)

    if df_obras.empty or df_cat.empty:
        st.warning("Cadastre ao menos uma obra e uma categoria.")
        return

    obras_dict = dict(zip(df_obras["descricao"], df_obras["id"]))
    categorias_dict = dict(zip(df_cat["descricao"], df_cat["id"]))
    # 1. Certifique-se de que está buscando os dados de fornecedores no início do render:
    df_fornecedores = listar_fornecedores(usuario_id)

# 2. Certifique-se de criar o dicionário mapeando os fornecedores:
    fornecedores_dict = dict(zip(df_fornecedores['nome'], df_fornecedores['id'])) if not df_fornecedores.empty else {}
    # =====================================================
    # BOTÃO NOVO LANÇAMENTO
    # =====================================================
    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("➕ Novo Lançamento"):
            abrir_modal_lancamento(
                usuario_id,
                obras_dict,
                categorias_dict,
                fornecedores_dict
            )

    # =====================================================
    # HISTÓRICO
    # =====================================================
    st.divider()
    st.subheader("📋 Últimos Lançamentos")

    df_hist = listar_lancamentos(usuario_id)

    if df_hist.empty:
        st.info("Nenhum lançamento encontrado.")
    else:
        st.dataframe(df_hist, use_container_width=True)

    # =====================================================
    # GRÁFICO
    # =====================================================
    st.divider()
    st.subheader("📊 Distribuição de Custos por Categoria")

    obra_grafico_nome = st.selectbox(
        "Selecione a obra para visualizar o gráfico",
        list(obras_dict.keys()),
        key="grafico_obra"
    )

    obra_grafico_id = obras_dict[obra_grafico_nome]

    df_resumo = resumo_por_categoria(usuario_id, obra_grafico_id)

    if not df_resumo.empty:

        fig = px.pie(
            df_resumo,
            names="categoria",
            values="total",
            hole=0.4,
        )

        fig.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<extra></extra>"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Sem dados suficientes para gerar o gráfico.")

# =====================================================
# MODAL NOVO LANÇAMENTO
# =====================================================
@st.dialog("Registrar Novo Lançamento")
def abrir_modal_lancamento(
    usuario_id,
    obras_dict,
    categorias_dict,
    fornecedores_dict # <-- Nome correto do parâmetro
):

    with st.form("form_lancamento_modal", clear_on_submit=True):

        col1, col2, col3 = st.columns(3)

        obra_nome = col1.selectbox(
            "Obra",
            list(obras_dict.keys()) if obras_dict else ["Nenhuma obra cadastrada"]
        )

        categoria_nome = col2.selectbox(
            "Categoria",
            list(categorias_dict.keys()) if categorias_dict else ["Nenhuma categoria cadastrada"]
        )

        fornecedor_nome = col3.selectbox(
            "Fornecedor",
            list(fornecedores_dict.keys()) if fornecedores_dict else ["Nenhum fornecedor cadastrado"]
        )

        material = st.text_input("Material")

        col4, col5, col6 = st.columns(3)

        medida = col4.selectbox(
            "Medida",
            ["Unidade", "Metro", "Kg", "Litro"]
        )

        qtd = col5.number_input(
            "Quantidade",
            min_value=0.01,
            step=0.01
        )

        v_unit = col6.number_input(
            "Valor Unitário",
            min_value=0.0,
            step=0.01
        )

        v_extra = st.number_input(
            "Valor Extra",
            min_value=0.0,
            step=0.01
        )

        data_l = st.date_input("Data")

        col_btn1, col_btn2 = st.columns(2)

        salvar = col_btn1.form_submit_button(
            "💾 Salvar",
            width="stretch"
        )

        cancelar = col_btn2.form_submit_button(
            "❌ Cancelar",
            width="stretch"
        )

        if salvar:
            if not material.strip():
                st.warning("Informe o material.")
                return
            
            # CORRIGIDO: alterado de "proveedores_dict" para "fornecedores_dict"
            if not obras_dict or not categorias_dict or not fornecedores_dict:
                st.error("Certifique-se de ter Obras, Categorias e Fornecedores cadastrados antes de lançar.")
                return

            # CORRIGIDO: alterado para buscar do dicionário em português de forma segura
            id_cat = categorias_dict.get(categoria_nome)
            id_obr = obras_dict.get(obra_nome)
            id_for = fornecedores_dict.get(fornecedor_nome)

            criar_lancamento(
                usuario_id=usuario_id,
                id_categoria=id_cat,
                id_obra=id_obr,
                fornecedor_id=id_for,
                material=material.strip(),
                tipo_medida=medida,
                quantidade=qtd,
                valor_unitario=v_unit,
                valor_extra=v_extra,
                data_lancamento=data_l
            )

            st.success("Lançamento registrado com sucesso!")
            st.rerun()

        if cancelar:
            st.rerun()