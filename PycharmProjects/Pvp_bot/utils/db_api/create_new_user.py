from psycopg2._psycopg import cursor

from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query, fetchall_query, fetchone_query


def create_new_user(user):
    query1 = f"SELECT * FROM users WHERE id = {user.id}"
    query2 = f"INSERT INTO users (id, name, username) VALUES({user.id}, '{user.first_name}', '{user.username}')"
    query3 = f"INSERT INTO deposits (user_id) VALUES({user.id})"

    connection = db_connection()
    try:
        user = fetchone_query(connection, query1)
        if not user:
            execute_query(connection, query2)
            print("Добавлен новый пользователь")
            execute_query(connection, query3)
            print("Пользователю выдан кошелёк")
        else:
            print("Пользователь существует")
    except:
        print("Ошибка при добавлении пользователя")
    close_connection(connection)
