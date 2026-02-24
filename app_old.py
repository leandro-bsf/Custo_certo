import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Photo Love - Gestão de Obras", layout="wide")

# --- GERENCIAMENTO DO BANCO DE DADOS (SQLite) ---
def init_db():
    conn = sqlite3.connect('gestao_obras.db', check_same_thread=False)
    c = conn.cursor()
    # Tabela de Categorias
    c.execute('''CREATE TABLE IF NOT EXISTS categorias 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT, data_criacao TEXT)''')
    # Tabela de Obras
    c.execute('''CREATE TABLE IF NOT EXISTS obras 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT, endereco TEXT, cidade TEXT, 
                  rua TEXT, numero TEXT, responsavel TEXT, contato TEXT, email TEXT, data_criacao TEXT)''')
    # Tabela de Lançamentos
    c.execute('''CREATE TABLE IF NOT EXISTS lancamentos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, id_categoria INTEGER, id_obra INTEGER, material TEXT, 
                  tipo_medida TEXT, quantidade REAL, valor_unitario REAL, valor_extra REAL, 
                  data_lancamento TEXT, FOREIGN KEY(id_categoria) REFERENCES categorias(id), 
                  FOREIGN KEY(id_obra) REFERENCES obras(id))''')
    conn.commit()
    return conn

conn = init_db()

# --- FUNÇÃO DE EXPORTAÇÃO PDF ---
def gerar_pdf(df, titulo_obra, tipo_relatorio):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    
    # Cabeçalho
    pdf.cell(190, 10, f"RELATORIO DE CUSTOS - {tipo_relatorio.upper()}", ln=True, align='C')
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(190, 8, f"Obra: {titulo_obra}", ln=True, align='C')
    pdf.cell(190, 8, f"Emissao: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)

    # Tabela
    pdf.set_font("Helvetica", "B", 10)
    col_width = 190 / len(df.columns)
    
    for col in df.columns:
        pdf.cell(col_width, 10, str(col), border=1, align='C')
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    col_custo = "Custo Total (R$)" if "Custo Total (R$)" in df.columns else "Subtotal"
    
    for _, row in df.iterrows():
        for val in row:
            text = str(val).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(col_width, 8, text, border=1)
        pdf.ln()
    
    # TOTALIZADOR NO PDF
    total_geral = df[col_custo].sum()
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(190, 10, f"TOTAL GERAL: R$ {total_geral:,.2f}", border=1, ln=True, align='R')
    
    return pdf.output()

# --- INTERFACE (MENU SUPERIOR) ---
st.title("🏗️ Sistema de Gestão de Obras")
tab_lanc, tab_obras, tab_cat = st.tabs(["Lançamentos", "Obras", "Categorias"])

# --- MENU CATEGORIAS ---
with tab_cat:
    st.header("Gerenciar Categorias")
    with st.form("form_categorias", clear_on_submit=True):
        desc = st.text_input("Descrição da Categoria")
        if st.form_submit_button("Salvar Categoria"):
            if desc:
                data_atual = datetime.now().strftime("%d/%m/%Y")
                conn.execute("INSERT INTO categorias (descricao, data_criacao) VALUES (?, ?)", (desc, data_atual))
                conn.commit()
                st.success("Categoria cadastrada!")
            else:
                st.error("Preencha a descrição.")

    st.subheader("Categorias Cadastradas")
    df_cat = pd.read_sql("SELECT * FROM categorias", conn)
    st.dataframe(df_cat, use_container_width=True)

# --- MENU OBRAS ---
with tab_obras:
    st.header("Gerenciar Obras")
    with st.expander("Cadastrar Nova Obra"):
        with st.form("form_obras", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nome_obra = col1.text_input("Nome/Descrição da Obra")
            responsavel = col2.text_input("Responsável")
            endereco = col1.text_input("Endereço")
            cidade = col2.text_input("Cidade")
            rua = col1.text_input("Rua")
            numero = col2.text_input("Número")
            contato = col1.text_input("Contato (Tel)")
            email = col2.text_input("E-mail")
            
            if st.form_submit_button("Cadastrar Obra"):
                data_criacao = datetime.now().strftime("%d/%m/%Y")
                conn.execute("""INSERT INTO obras (descricao, endereco, cidade, rua, numero, responsavel, contato, email, data_criacao) 
                             VALUES (?,?,?,?,?,?,?,?,?)""", 
                             (nome_obra, endereco, cidade, rua, numero, responsavel, contato, email, data_criacao))
                conn.commit()
                st.success("Obra cadastrada com sucesso!")

    st.subheader("Lista de Obras")
    df_obras = pd.read_sql("SELECT * FROM obras", conn)
    st.dataframe(df_obras, use_container_width=True)

    st.divider()
    st.subheader("📑 Resumos e Custos")
    obra_selecionada = st.selectbox("Selecione uma obra para ver o resumo", df_obras['descricao'].tolist())
    
    if obra_selecionada:
        id_obra = df_obras[df_obras['descricao'] == obra_selecionada]['id'].values[0]
        
        c1, c2 = st.columns(2)
        
        # RESUMO AGRUPADO
        if c1.button("Resumo Agrupado (Materiais)"):
            query = f"""SELECT material as "Material", SUM(quantidade) as "Qtd", tipo_medida as "Unidade", 
                        SUM((quantidade * valor_unitario) + valor_extra) as "Custo Total (R$)"
                        FROM lancamentos WHERE id_obra = {id_obra} GROUP BY material"""
            res_df = pd.read_sql(query, conn)
            if not res_df.empty:
                st.table(res_df)
                total = res_df["Custo Total (R$)"].sum()
                st.metric("Total Acumulado", f"R$ {total:,.2f}")
                pdf_bytes = gerar_pdf(res_df, obra_selecionada, "Agrupado")
                st.download_button("Descargar PDF Agrupado", data=bytes(pdf_bytes), file_name="resumo_agrupado.pdf", mime="application/pdf")
            else:
                st.info("Sem lançamentos para esta obra.")

        # RESUMO DETALHADO
        if c2.button("Resumo Detalhado (Linha a Linha)"):
            query = f"""SELECT data_lancamento as "Data", material as "Material", quantidade as "Qtd", 
                        valor_unitario as "V. Unit", valor_extra as "Extra",
                        ((quantidade * valor_unitario) + valor_extra) as "Subtotal"
                        FROM lancamentos WHERE id_obra = {id_obra}"""
            det_df = pd.read_sql(query, conn)
            if not det_df.empty:
                st.dataframe(det_df, use_container_width=True)
                total_det = det_df["Subtotal"].sum()
                st.metric("Total Detalhado", f"R$ {total_det:,.2f}")
                pdf_bytes_det = gerar_pdf(det_df, obra_selecionada, "Detalhado")
                st.download_button("Descargar PDF Detalhado", data=bytes(pdf_bytes_det), file_name="resumo_detalhado.pdf", mime="application/pdf")
            else:
                st.info("Sem lançamentos para esta obra.")

# --- MENU LANÇAMENTOS ---
with tab_lanc:
    st.header("Novo Lançamento")
    
    if df_obras.empty or df_cat.empty:
        st.warning("Cadastre primeiro ao menos uma Obra e uma Categoria.")
    else:
        with st.form("form_lanc", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            obra_nome = col_a.selectbox("Vincular Obra", df_obras['descricao'].tolist())
            cat_nome = col_b.selectbox("Categoria", df_cat['descricao'].tolist())
            
            mat = st.text_input("Descrição do Material")
            
            col_c, col_d, col_e = st.columns(3)
            medida = col_c.selectbox("Medida", ["Unidade", "Metro Quadrado", "Metro Linear", "Kg", "Litro"])
            qtd = col_d.number_input("Quantidade", min_value=0.01)
            v_unit = col_e.number_input("Valor Unitário (R$)", min_value=0.0)
            
            v_extra = st.number_input("Valor Extra/Frete (R$)", min_value=0.0)
            data_l = st.date_input("Data do Lançamento", datetime.now())
            
            if st.form_submit_button("Confirmar Lançamento"):
                id_o = int(df_obras[df_obras['descricao'] == obra_nome]['id'].values[0])
                id_c = int(df_cat[df_cat['descricao'] == cat_nome]['id'].values[0])
                
                conn.execute("""INSERT INTO lancamentos 
                             (id_categoria, id_obra, material, tipo_medida, quantidade, valor_unitario, valor_extra, data_lancamento) 
                             VALUES (?,?,?,?,?,?,?,?)""", 
                             (id_c, id_o, mat, medida, qtd, v_unit, v_extra, data_l.strftime("%d/%m/%Y")))
                conn.commit()
                st.success("Lançamento realizado!")

    st.subheader("Histórico Geral de Lançamentos")
    df_history = pd.read_sql("SELECT * FROM lancamentos ORDER BY id DESC LIMIT 10", conn)
    st.dataframe(df_history, use_container_width=True)