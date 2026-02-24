import streamlit as st
from crud.obras_crud import criar_obra, listar_obras
from crud.lancamentos_crud import resumo_agrupado, resumo_detalhado, resumo_por_categoria
from utils import pdf_generator
# =====================================================
# RENDER PRINCIPAL
# =====================================================
def render(usuario_id):

    st.subheader("🏗️ Obras")

    # =====================================================
    # BOTÃO NOVA OBRA
    # =====================================================
    col1, col2 = st.columns([6, 1])

    with col2:
        if st.button("➕ Nova Obra"):
            abrir_modal_obra(usuario_id)

    # =====================================================
    # LISTAGEM
    # =====================================================
    df_obras = listar_obras(usuario_id)

    if df_obras.empty:
        st.info("Nenhuma obra cadastrada.")
        return

    st.dataframe(df_obras, use_container_width=True)

    # =====================================================
    # RESUMOS
    # =====================================================
    st.divider()
    st.subheader("📊 Resumo Financeiro")

    obras_dict = {
        row["descricao"]: row["id"]
        for _, row in df_obras.iterrows()
    }

    obra_nome = st.selectbox(
        "Selecione a obra",
        list(obras_dict.keys())
    )

    obra_id = obras_dict[obra_nome]

    valor_contratado = df_obras[
        df_obras["id"] == obra_id
    ]["valor_contratado"].values[0]

    tipo_resumo = st.radio(
        "Tipo de Resumo",
        ["Agrupado", "Detalhado"],
        horizontal=True
    )

    if tipo_resumo == "Agrupado":
        df_res = resumo_agrupado(usuario_id, obra_id)

        if df_res.empty:
            st.warning("Sem lançamentos encontrados.")
            return

        st.dataframe(df_res, use_container_width=True)
        total_gasto = df_res["Custo Total (R$)"].sum()

    else:
        df_res = resumo_detalhado(usuario_id, obra_id)

        if df_res.empty:
            st.warning("Sem lançamentos encontrados.")
            return

        st.dataframe(df_res, use_container_width=True)
        total_gasto = df_res["Subtotal"].sum()

    # =====================================================
    # MÉTRICAS FINANCEIRAS
    # =====================================================
    lucro = valor_contratado - total_gasto
    margem = (lucro / valor_contratado * 100) if valor_contratado > 0 else 0

    st.divider()

    col_a, col_b, col_c = st.columns(3)

    col_a.metric(
        "Valor Contratado",
        f"R$ {valor_contratado:,.2f}"
    )

    col_b.metric(
        "Total Gasto",
        f"R$ {total_gasto:,.2f}"
    )

    col_c.metric(
        "Lucro",
        f"R$ {lucro:,.2f}",
        delta=f"{margem:.1f}%",
        delta_color="normal" if lucro >= 0 else "inverse"
    )
# =====================================================
# EXPORTAR RELATÓRIO PDF
# =====================================================
    st.divider()
    st.subheader("📄 Exportar Relatório Completo")

    # Gerar dados do gráfico por categoria
    df_categoria = resumo_por_categoria(usuario_id, obra_id)

    if df_res.empty:
        st.warning("Não há dados suficientes para gerar o relatório.")
    else:

        col_btn, col_info = st.columns([1, 2])

        with col_btn:
            pdf_file = pdf_generator.gerar_pdf_obra(
                obra_nome,
                valor_contratado,
                total_gasto,
                lucro,
                margem,
                df_res,
                df_categoria  # <- novo parâmetro
            )

            st.download_button(
                label="📥 Baixar PDF",
                data=pdf_file,
                file_name=f"relatorio_{obra_nome}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col_info:
            st.caption(
                "O relatório inclui resumo financeiro, gráfico de distribuição "
                "de custos por categoria e detalhamento completo dos lançamentos."
            )

# =====================================================
# MODAL NOVA OBRA
# =====================================================
@st.dialog("Cadastrar Nova Obra")
def abrir_modal_obra(usuario_id):

    with st.form("form_obra_modal"):

        col1, col2 = st.columns(2)

        descricao = col1.text_input("Nome da Obra")
        responsavel = col2.text_input("Responsável")

        endereco = col1.text_input("Endereço")
        cidade = col2.text_input("Cidade")

        contato = col1.text_input("Contato")
        email = col2.text_input("Email")

        status = st.selectbox(
            "Status",
            [
                "Planejamento",
                "Aprovada_Licencas",
                "Em_Execucao",
                "Acabamento",
                "Finalizada"
            ]
        )

        valor_contratado = st.number_input(
            "Valor Contratado (R$)",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        col_btn1, col_btn2 = st.columns(2)

        salvar = col_btn1.form_submit_button(
            "💾 Salvar",
            use_container_width=True
        )

        cancelar = col_btn2.form_submit_button(
            "❌ Cancelar",
            use_container_width=True
        )

        if salvar:
            if not descricao.strip():
                st.warning("Informe o nome da obra.")
            else:
                criar_obra(
                    usuario_id,
                    descricao.strip(),
                    endereco.strip(),
                    cidade.strip(),
                    responsavel.strip(),
                    contato.strip(),
                    email.strip(),
                    status,
                    valor_contratado
                )
                st.success("Obra cadastrada com sucesso!")
                st.rerun()

        if cancelar:
            st.rerun()