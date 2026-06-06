import sqlite3

def get_connection():
    return sqlite3.connect("gestao_obras.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # USUÁRIOS
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            senha TEXT,
            data_criacao TEXT
        )
    """)

    # CATEGORIAS
    c.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            descricao TEXT,
            data_criacao TEXT
        )
    """)

    # OBRAS
    c.execute("""
        CREATE TABLE IF NOT EXISTS obras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            descricao TEXT,
            endereco TEXT,
            cidade TEXT,
            responsavel TEXT,
            contato TEXT,
            email TEXT,
            data_criacao TEXT,
            status TEXT CHECK(status IN (
                'Planejamento',
                'Aprovada_Licencas',
                'Em_Execucao',
                'Acabamento',
                'Finalizada'
            )) DEFAULT 'Planejamento',
            valor_contratado REAL DEFAULT 0
        )
    """)
    # FORNECEDOR
    c.execute("""
            CREATE  TABLE IF NOT EXISTS  fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                cnpj TEXT,
                telefone TEXT,
                email TEXT,
                cidade TEXT,
                observacao TEXT,
                data_criacao TEXT
            );
              """)

    # LANÇAMENTOS
    c.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            id_categoria INTEGER,
            id_obra INTEGER,
            material TEXT,
            tipo_medida TEXT,
            quantidade REAL,
            valor_unitario REAL,
            valor_extra REAL,
            data_lancamento TEXT
        )
    """)

    conn.commit()
    conn.close()