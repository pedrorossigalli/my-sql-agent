import re
import sqlite3
from anthropic import Anthropic
from database import get_connection

block = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|PRAGMA|REPLACE)\b"


class SqlSemPermissaoError(Exception):
    """Raise quando a operação no Banco de Dados é inválida"""
    def __init__(self, message="Operacao invalida no banco de dados"):
        self.message = message
        super().__init__(self.message)


def validar_sql_leitura(query):
    new_query = query.strip().rstrip(";")

    if not new_query.lower().startswith("select"):
        raise SqlSemPermissaoError

    if ";" in new_query:
        raise SqlSemPermissaoError

    if re.search(block, new_query):
        raise SqlSemPermissaoError

    return new_query


def run_sql_query(query):
    validar_sql_leitura(query)
    
    with get_connection() as connection:
        # Transforma o retorno de fetch para um objeto Row
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        # Tranforma cada linha em um dicionário
        rows = [dict(row) for row in rows]

    connection.close()


def get_info_tabelas():
    """Retorna o nome de todas as tabelas do Banco de Dados junto de todos os seus atributos em uma única string"""
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()    

        # BD do SQLite guardando as informações do BD do projeto. Dentro existe a tabela sqlite_sequence que guarda a informação dos incrementos de AUTOINCREMENT das tabelas, por isso ela é excluída da query.
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_sequence'")
        table_names = cursor.fetchall()
        table_names = [dict(table_name) for table_name in table_names]

        for table_name in table_names:
            print(table_name['name'])
            cursor.execute(f"PRAGMA table_info({table_name['name']})")
            table_info = cursor.fetchall()
            table_info = [dict(column) for column in table_info]
            print(table_info)
            complete_table_description += f"{table_name['name']}("
            for index, column in enumerate(table_info):
                # Diferente do ultimo elemento da lista
                if index != len(table_info) - 1:
                    complete_table_description += f"{column['name']}, "
                else:
                    complete_table_description += f"{column['name']}) "

    connection.close()
    return complete_table_description


def run_tool():
    pass

if __name__ == "__main__":
    pass