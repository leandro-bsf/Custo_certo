import pandas as pd
from database import get_connection
from datetime import datetime


def criar_fornecedor(
    usuario_id,
    nome,
    cnpj,
    telefone,
    email,
    cidade,
    observacao
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO fornecedores
        (
            usuario_id,
            nome,
            cnpj,
            telefone,
            email,
            cidade,
            observacao,
            data_criacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        nome,
        cnpj,
        telefone,
        email,
        cidade,
        observacao,
        datetime.now().strftime("%d/%m/%Y")
    ))

    conn.commit()
    conn.close()


def listar_fornecedores(usuario_id):
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM fornecedores
        WHERE usuario_id = ?
        ORDER BY nome
        """,
        conn,
        params=(usuario_id,)
    )

    conn.close()
    return df


def buscar_fornecedor_por_nome(usuario_id, nome):
    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT id
        FROM fornecedores
        WHERE usuario_id = ?
        AND nome = ?
        """,
        (usuario_id, nome)
    )

    fornecedor = cursor.fetchone()

    conn.close()

    return fornecedor[0] if fornecedor else None


def buscar_fornecedor_por_id(fornecedor_id):
    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT *
        FROM fornecedores
        WHERE id = ?
        """,
        (fornecedor_id,)
    )

    fornecedor = cursor.fetchone()

    conn.close()

    return fornecedor


def atualizar_fornecedor(
    fornecedor_id,
    nome,
    cnpj,
    telefone,
    email,
    cidade,
    observacao
):
    conn = get_connection()

    conn.execute("""
        UPDATE fornecedores
        SET
            nome = ?,
            cnpj = ?,
            telefone = ?,
            email = ?,
            cidade = ?,
            observacao = ?
        WHERE id = ?
    """, (
        nome,
        cnpj,
        telefone,
        email,
        cidade,
        observacao,
        fornecedor_id
    ))

    conn.commit()
    conn.close()


def excluir_fornecedor(fornecedor_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM fornecedores WHERE id = ?",
        (fornecedor_id,)
    )

    conn.commit()
    conn.close()