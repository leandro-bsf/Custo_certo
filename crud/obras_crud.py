import pandas as pd
from database import get_connection
from datetime import datetime

def criar_obra(usuario_id, descricao, endereco, cidade, responsavel, contato, email):
    conn = get_connection()
    conn.execute("""
        INSERT INTO obras 
        (usuario_id, descricao, endereco, cidade, responsavel, contato, email, data_criacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        descricao,
        endereco,
        cidade,
        responsavel,
        contato,
        email,
        datetime.now().strftime("%d/%m/%Y")
    ))
    conn.commit()
    conn.close()


def listar_obras(usuario_id):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM obras WHERE usuario_id = ? ORDER BY id DESC",
        conn,
        params=(usuario_id,)
    )
    conn.close()
    return df


def buscar_obra_por_nome(usuario_id, descricao):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT id FROM obras WHERE usuario_id=? AND descricao=?",
        (usuario_id, descricao)
    )
    obra = cursor.fetchone()
    conn.close()
    return obra[0] if obra else None