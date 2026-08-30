import csv
import sqlite3
from pathlib import Path

DB_PATH = "data/empresa.db"


def get_connection():
    """Retorna a conexão com o BD com PRAGMA ativado."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def criar_tabelas():
    """Cria as tabelas Materiais, Clientes e Pesagens caso não existam."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS Materiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco_por_tonelada REAL NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cnpj TEXT,
                cpf TEXT,

                CONSTRAINT cnpj_or_cpf
                    CHECK (
                        (cnpj IS NOT NULL AND cpf IS NULL)
                        OR
                        (cnpj IS NULL AND cpf IS NOT NULL)
                    )
            )
        """)

        connection.execute("""
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
    connection.close()


def popular_materiais():
    """Popula a tabela de Materiais a partir do CSV."""
    with get_connection() as connection:
        sql = "INSERT INTO Materiais (nome, preco_por_tonelada) VALUES (?, ?)"

        # Abre o CSV e coloca os valores em uma lista de dicionarios 
        with open("data/materiais.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Lista de Tuples com info de materiais.csv
            many_materiais = [(str(row["nome"]), float(row["preco_por_tonelada"])) for row in reader]

        connection.executemany(sql, many_materiais)
    connection.close()


def popular_clientes():
    """Popula a tabela de Clientes a partir do CSV."""
    with get_connection() as connection:
        sql = "INSERT INTO Clientes (nome, cnpj, cpf) VALUES (?, ?, ?)"

        with open("data/clientes.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Lista de Tuples com info de clientes.csv
            many_clientes = [(str(row["nome"]), str(row["cnpj"]) or None, str(row["cpf"]) or None) for row in reader]

        connection.executemany(sql, many_clientes)
    connection.close()


def popular_pesagens():
    """Popula a tabela de Pesagens a partir do CSV."""
    with get_connection() as connection:
        sql = "INSERT INTO Pesagens (cliente_id, material_id, data, peso, preco_na_data) VALUES (?, ?, ?, ?, ?)"

        with open("data/pesagens.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Lista de Tuples com info de pesagens.csv
            many_pesagens = [(int(row["cliente_id"]), int(row["material_id"]), str(row["data"]), float(row["peso"]), float(row["preco_na_data"])) for row in reader]

        connection.executemany(sql, many_pesagens)
    connection.close()


if __name__ == "__main__":
    # Se o banco de dados já existe, o script não será executado
    if Path(DB_PATH).exists():
        print("Banco de dados já existe, nada a fazer.")
    else:
        criar_tabelas()
        popular_materiais()
        popular_clientes()
        popular_pesagens()
        print("Banco criado e populado com sucesso.")