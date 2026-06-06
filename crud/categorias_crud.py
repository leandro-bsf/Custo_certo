import pandas as pd
from database import get_connection
from datetime import datetime

def criar_categoria(usuario_id, descricao):
    conn = get_connection()
    conn.execute(
        "INSERT INTO categorias (usuario_id, descricao, data_criacao) VALUES (?, ?, ?)",
        (usuario_id, descricao, datetime.now().strftime("%d/%m/%Y"))
    )
    conn.commit()
    conn.close()

def listar_categorias(usuario_id):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT id, descricao, data_criacao FROM categorias WHERE usuario_id=?",
        conn,
        params=(usuario_id,)
    )
    conn.close()
    return df