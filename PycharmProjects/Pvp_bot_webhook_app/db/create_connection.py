import psycopg2
from psycopg2 import Error

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


def connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        print("Connection to PostgreSQL DB successful")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return connection


def close_connection(connection):
    cursor = connection.cursor()
    cursor.close()
    connection.close()


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except:
        print(f"The error occurred")


def fetchall_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        print(f"The error occurred")


def fetchone_query(connection, query):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(query)
        return cursor.fetchone()
    except:
        print(f"The error occurred")


def mogrify_query(connection, query, list_object1, list_object2):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.mogrify(query, (list_object1, list_object2))
        return cursor.fetchone()
    except:
        print(f"The error occurred")


def print_query(connection, query):
    cursor = connection.cursor()
    try:
        print(query)
        cursor.execute(query)
        print(cursor)
        print("Query executed successfully")
    except:
        print(f"The error occurred")