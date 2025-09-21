import sqlite3
import os

DATABASE_FILE = 'database.db'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

def init_db():
    """Inicializa o banco de dados, criando a tabela de usuários se não existir."""
    if not os.path.exists(DATABASE_FILE):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Adiciona um usuário padrão para teste
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('testuser', 'password123'))
        conn.commit()
        conn.close()
        print("Banco de dados inicializado e usuário 'testuser' criado.")
    else:
        print("Banco de dados já existe.")

if __name__ == '__main__':
    # Quando o script é executado diretamente, ele inicializa o DB
    init_db()