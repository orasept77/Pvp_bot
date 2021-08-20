from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query, fetchall_query, print_query, fetchone_query


def check_is_room_is_full_and_not_aborted(room_number):
    check_room_is_full_query = f"""
    SELECT * from rooms WHERE rooms.id = {room_number[0]}
    """
    connection = db_connection()
    try:
        room_info = fetchone_query(connection, check_room_is_full_query)
        print(room_info)
        if room_info[1] is not None and room_info[2] is not None:
            return True
    except:
        print("Ошибка при проверке заполненности комнаты.")
    close_connection(connection)


def change_room_state_on_playing(room_number):
    print(room_number)
    change_room_state_query = f"""
    UPDATE rooms SET room_state = 'PLAYING' WHERE id = {room_number[0]}
    """

    connection = db_connection()
    try:
        execute_query(connection, change_room_state_query)
    except:
        print("Ошибка при смене стейта комнаты на 'Играют'.")
    close_connection(connection)


def change_room_state_on_ended(room_number):
    change_room_state_query = f"""
    UPDATE rooms SET room_state = 'ENDED' WHERE id = {room_number[0]}
    """

    connection = db_connection()
    try:
        execute_query(connection, change_room_state_query)
    except:
        print("Ошибка при смене стейта комнаты на 'Законченна'.")
    close_connection(connection)


def change_room_state_on_aborted(room_number):
    change_room_state_query = f"""
    UPDATE rooms SET room_state = 'ABORTED' WHERE id = {room_number[0]}
    """

    connection = db_connection()
    try:
        execute_query(connection, change_room_state_query)
    except:
        print("Ошибка при смене стейта комнаты на 'Заброшенна'.")
    close_connection(connection)
