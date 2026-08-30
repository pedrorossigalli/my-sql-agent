import sqlite3

DB_PATH="data/empresa.db"

# cliente: id, nome, cnpj, cpf
# materiais: id, nome_material, preco_por_tonelada
# pesagens: id, clientes_id (referencia cliente), material_id (referencia materiais), data, peso

def criar_tabelas():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()
    connection.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Materiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco_por_tonelada REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT,
            cpf TEXT,

            CONSTRAINT cnpj_or_cpf
                CHECK (
                    (cnpj IS NOT NULL AND cpf IS NULL)
                    OR
                    (cnpj is NULL AND cpf IS NOT NULL)
                )
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pesagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            material_id INTEGER,
            data TEXT NOT NULL,
            peso REAL NOT NULL,
            preco_na_data REAL NOT NULL,

            FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
            FOREIGN KEY (material_id) REFERENCES Materiais(id)
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    criar_tabelas()