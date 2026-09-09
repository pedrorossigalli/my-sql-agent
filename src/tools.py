import re
import sqlite3
from anthropic import Anthropic
from .database import get_connection

block = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|PRAGMA|REPLACE)\b"

TOOLS_SCHEMA = [
    {
        "name": "run_sql_query",
        "description": "Executa uma consulta no banco de dados e retorna uma lista em que cada elemento é um dicionário de cada linha",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Uma única consulta em SQL, e.g. SELECT * FROM Materiais WHERE preco_por_tonelada > 50"
                }
            },
            "required": ["query"]
        }   
    },
    {
        "name": "get_info_tabelas",
        "description": "Retorna o nome e atributos de todo o banco de dados, no modelo Nome(atributo1, atributo2, ...) para quando não houver contexto de quais são as tabelas e atributos dela.",
        "input_schema": {
            "type": "object",
            "properties": {},
        } 
    }
]

class SqlSemPermissaoError(Exception):
    """Levanta um erro quando a operação no banco de dados é inválida"""
    def __init__(self, message="Operacao invalida no banco de dados"):
        self.message = message
        super().__init__(self.message)


def validar_sql_leitura(query: str):
    """Levanta um erro quando a query não atende as exigências de segurança"""
    new_query = query.strip().rstrip(";")

    if not new_query.lower().startswith("select"):
        raise SqlSemPermissaoError

    if ";" in new_query:
        raise SqlSemPermissaoError

    if re.search(block, new_query):
        raise SqlSemPermissaoError


def run_sql_query(query: str) -> list[dict[str, float]]:
    """Retorna uma lista de dicionários com as linhas da tabela que atendem a query"""
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
    return rows


def get_info_tabelas() -> str:
    """Retorna o nome de todas as tabelas do Banco de Dados junto de todos os seus atributos em uma única string"""
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()    

        complete_table_description = ""

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


def run_tool(tool_name: str, tool_input: dict):
    match tool_name:
        case "run_sql_query":
            query = tool_input["query"]
            try:
                return run_sql_query(query)
            except SqlSemPermissaoError:
                return {"erro": "Erro na consulta! Sem permissão."}
        case "get_info_tabelas":
            return get_info_tabelas()
        case _:
            return {"erro": f"Ferramenta desconhecida: {tool_name}"}


if __name__ == "__main__":
    print(run_sql_query("SELECT * FROM Materiais"))