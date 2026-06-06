import pandas as pd
from database import get_connection
from datetime import datetime

def criar_lancamento(usuario_id, id_categoria, id_obra, material,
                     tipo_medida, quantidade, valor_unitario,
                     valor_extra, data_lancamento,fornecedor_id):

    conn = get_connection()
    conn.execute("""
        INSERT INTO lancamentos
        (usuario_id, id_categoria, id_obra, material,
         tipo_medida, quantidade, valor_unitario,
         valor_extra, data_lancamento,fornecedor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        id_categoria,
        id_obra,
        material,
        tipo_medida,
        quantidade,
        valor_unitario,
        valor_extra,
        data_lancamento.strftime("%d/%m/%Y"),
        fornecedor_id
    ))
    conn.commit()
    conn.close()


def listar_lancamentos(usuario_id):
    conn = get_connection()
    df = pd.read_sql("""
    SELECT 
            l.id,
            o.descricao AS obra,
            c.descricao AS categoria,
            l.material,
            l.tipo_medida,
            l.quantidade,
            l.valor_unitario,
            l.valor_extra,
            l.data_lancamento,
            fornecedor_id
        FROM lancamentos l
        JOIN obras o ON l.id_obra = o.id
        JOIN categorias c ON l.id_categoria = c.id
        WHERE l.usuario_id = ?
        ORDER BY l.id DESC
        LIMIT 10
    """, conn, params=(usuario_id,))
    conn.close()
    return df

def resumo_agrupado(usuario_id, obra_id):
    print(f"Gerando resumo agrupado para usuário_id={usuario_id} e obra_id={obra_id}")
    conn = get_connection()

    query = """
        SELECT l.material as "Material",
               SUM(l.quantidade) as "Qtd",
               l.tipo_medida as "Unidade",
               SUM((l.quantidade * l.valor_unitario) + l.valor_extra) 
               as "Custo Total (R$)"
        FROM lancamentos l
        JOIN obras o ON l.id_obra = o.id
        WHERE l.usuario_id = ?
        AND l.id_obra = ?
        GROUP BY l.material, l.tipo_medida
    """

    df = pd.read_sql(query, conn, params=(usuario_id, obra_id))
    print(df)
    conn.close()
    return df

def resumo_detalhado(usuario_id, obra_id):
    conn = get_connection()

    query = """
        SELECT l.data_lancamento as "Data",
               l.material as "Material",
               l.quantidade as "Qtd",
               l.valor_unitario as "V. Unit",
               l.valor_extra as "Extra",
               ((l.quantidade * l.valor_unitario) + l.valor_extra)
               as "Subtotal"
        FROM lancamentos l
        WHERE l.usuario_id = ?
        AND l.id_obra = ?
    """

    df = pd.read_sql(query, conn, params=(usuario_id, obra_id))
    conn.close()
    return df


def resumo_por_categoria(usuario_id, obra_id):
    conn = get_connection()

    query = """
        SELECT 
            c.descricao as categoria,
            SUM((l.quantidade * l.valor_unitario) + l.valor_extra) as total
        FROM lancamentos l
        JOIN categorias c ON l.id_categoria = c.id
        WHERE l.usuario_id = ?
        AND l.id_obra = ?
        GROUP BY c.descricao
    """

    df = pd.read_sql(query, conn, params=(usuario_id, obra_id))
    conn.close()
    return df