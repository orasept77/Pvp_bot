import asyncio

from psycopg2._psycopg import cursor

from games.blackjack.game import game_started
from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query, fetchall_query, print_query, fetchone_query


async def find_lobby_blackjack(user_id, rates_id, chat_id):
    find_lobby_query = f"""
    SELECT * FROM blackjack_lobby WHERE rates_id = {rates_id}
    """

    create_lobby_query = f"""
    INSERT INTO blackjack_lobby (user_id, rates_id, chat_id) VALUES ({user_id}, {rates_id}, {chat_id})
    """

    connection = db_connection()
    try:
        lobby = fetchone_query(connection, find_lobby_query)
        if not lobby:
            # Создаём лобби если список лобби пуст
            try:
                execute_query(connection, create_lobby_query)
                # Возвращаем номер лобби что-бы потом его удалить
            except:
                print("Ошибка в создании лобби")
        else:
            # Если нашли лобби - соединяем игроков в одну игру
            # Забираем ИД второго игрока из искаемого лобби
            second_user_id = lobby[0]
            second_user_chat_id = lobby[2]
            connect_players_lobby = f"""
            WITH game AS (
                INSERT INTO blackjack_game(rates_id, user_step_id) VALUES ({int(rates_id)}, {user_id})
                RETURNING id
            )
                SELECT id FROM game
            """
            game_id = fetchone_query(connection, connect_players_lobby)
            connect_players_lobby_2 = f"""
                INSERT INTO blackjack_game_user(user_id, game_id, chat_id) VALUES ({user_id}, {game_id[0]}, {chat_id});
                INSERT INTO blackjack_game_user(user_id, game_id, chat_id) VALUES ({second_user_id}, {game_id[0]}, {second_user_chat_id});
                INSERT INTO blackjack_game_dealer(game_id) VALUES ({game_id[0]});
            """
            execute_query(connection, connect_players_lobby_2)

            return game_id[0]
    except:
        print("Ошибка в поиске или создании лобби")
    close_connection(connection)


def delete_lobby_blackjack(user_id):
    delete_lobby_query = f"""
    DELETE FROM blackjack_lobby WHERE user_id = {user_id}
    """
    connection = db_connection()
    execute_query(connection, delete_lobby_query)
    close_connection(connection)
