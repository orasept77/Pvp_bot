import psycopg2
import psycopg2.extras
from psycopg2._psycopg import OperationalError


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def fetchall_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def fetchone_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(query)
        return cursor.fetchone()
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def print_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print(cursor.fetchall())
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")