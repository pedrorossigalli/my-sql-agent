import re
import sqlite3
from .database import get_connection

bloquear = r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|PRAGMA|REPLACE)\b"


class SqlSemPermissaoError(Exception):
    """Raise quando a operação no Banco de Dados é inválida"""
    def __init__(self, message="Operação inválida no banco de dados"):
        self.message = message
        super().__init__(self.message)


def validar_sql_leitura(query):
    new_query = query.strip().rstrip(";")

    if not new_query.lower().startswith("select"):
        raise SqlSemPermissaoError

    if ";" in new_query:
        raise SqlSemPermissaoError

    if re.search(bloquear, new_query):
        raise SqlSemPermissaoError

    return new_query