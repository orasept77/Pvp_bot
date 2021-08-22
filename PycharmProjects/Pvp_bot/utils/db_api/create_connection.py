import psycopg2
from psycopg2 import OperationalError


def connection_settings(conn_str):
    connection = None
    try:
        connection = psycopg2.connect(
            conn_str
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{format(str(e))}' occurred")
    return connection


def db_connection():
    return connection_settings(
        "postgres://postgres:123123123@144.91.110.3:5432/postgres"
    )