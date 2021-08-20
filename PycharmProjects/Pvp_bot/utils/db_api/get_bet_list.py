from psycopg2._psycopg import cursor

from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query, fetchall_query, print_query, fetchone_query


def get_bets_list():
    find_lobby_query = f"""
    SELECT * FROM rates
    """


    connection = db_connection()
    try:
         return fetchall_query(connection, find_lobby_query)
    except:
        print("Ошибка в поиске или создании лобби")
    close_connection(connection)