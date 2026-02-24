from database import get_connection
from datetime import datetime

def criar_usuario(email, senha):
    conn = get_connection()
    conn.execute(
        "INSERT INTO usuarios (email, senha, data_criacao) VALUES (?, ?, ?)",
        (email, senha, datetime.now().strftime("%d/%m/%Y"))
    )
    conn.commit()
    conn.close()

def autenticar_usuario(email, senha):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT id, email FROM usuarios WHERE email=? AND senha=?",
        (email, senha)
    )
    user = cursor.fetchone()
    conn.close()
    return user