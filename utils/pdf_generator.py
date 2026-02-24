import io
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import plotly.express as px


def gerar_pdf_obra(
    obra_nome,
    valor_contratado,
    total_gasto,
    lucro,
    margem,
    df_resumo,
    df_categoria  # <- novo parâmetro
):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []
    styles = getSampleStyleSheet()

    # ============================
    # TÍTULO
    # ============================
    elements.append(
        Paragraph(
            f"<b>Relatório Financeiro - {obra_nome}</b>",
            styles["Title"]
        )
    )
    elements.append(Spacer(1, 0.3 * inch))

    data_emissao = datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(
        Paragraph(
            f"Data de emissão: {data_emissao}",
            styles["Normal"]
        )
    )
    elements.append(Spacer(1, 0.3 * inch))

    # ============================
    # RESUMO FINANCEIRO
    # ============================
    resumo_data = [
        ["Valor Contratado", f"R$ {valor_contratado:,.2f}"],
        ["Total Gasto", f"R$ {total_gasto:,.2f}"],
        ["Lucro", f"R$ {lucro:,.2f}"],
        ["Margem", f"{margem:.1f}%"],
    ]

    resumo_table = Table(resumo_data, colWidths=[220, 150])
    resumo_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ]))

    elements.append(resumo_table)
    elements.append(Spacer(1, 0.5 * inch))

   # ============================
# GRÁFICO DE CATEGORIAS
# ============================
    if not df_categoria.empty:

        fig = px.pie(
            df_categoria,
            names="categoria",
            values="total",
            hole=0.5,
            color="categoria",
            color_discrete_sequence=px.colors.qualitative.Set3  # cores bonitas
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )

        fig.update_layout(
            width=800,
            height=600,
            showlegend=True,
            legend_title="Categorias",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(
                family="Arial",
                size=14,
                color="#2c3e50"
            ),
            margin=dict(t=60, b=40, l=40, r=40)
        )

        # Exporta em alta resolução
        img_bytes = fig.to_image(format="png", scale=2)
        img_buffer = io.BytesIO(img_bytes)

        elements.append(
            Paragraph("<b>Distribuição de Custos por Categoria</b>", styles["Heading2"])
        )
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(
            Image(img_buffer, width=5.5 * inch, height=4.2 * inch)
        )

        elements.append(Spacer(1, 0.5 * inch))

    # ============================
    # TABELA DE LANÇAMENTOS
    # ============================
    data = [list(df_resumo.columns)] + df_resumo.values.tolist()

    tabela = Table(data, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
    ]))

    elements.append(
        Paragraph("<b>Detalhamento dos Lançamentos</b>", styles["Heading2"])
    )
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(tabela)

    doc.build(elements)
    buffer.seek(0)

    return buffer