from psycopg2._psycopg import cursor

from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query, fetchall_query, print_query, fetchone_query


def find_lobby_blackjack(user_id, rates_id):
    find_lobby_query = f"""
    SELECT * FROM blackjack_lobby WHERE rates_id = {rates_id}
    """

    create_lobby_query = f"""
    INSERT INTO blackjack_lobby (user_id, rates_id) VALUES ({user_id}, {rates_id})
    """

    connection = db_connection()
    try:
        lobby = fetchone_query(connection, find_lobby_query)
        if not lobby:
            # Создаём лобби если список лобби пуст
            try:
                execute_query(connection, create_lobby_query)
            except:
                print("Ошибка в создании лобби")
        else:
            # Если нашли лобби - соединяем игроков в одну игру
            # Забираем ИД второго игрока из искаемого лобби
            second_user_id = lobby[0]
            connect_players_lobby = f"""
            WITH game AS (
                INSERT INTO blackjack_game(rates_id, user_step_id) VALUES ({rates_id, user_id})
                RETURNING id
            )
                INSERT INTO blackjack_game_user(user_id, game_id) VALUES ({user_id}, (SELECT id FROM room))
                INSERT INTO blackjack_game_user(user_id, game_id) VALUES ({second_user_id}, (SELECT id FROM room))
                INSERT INTO blackjack_game_dealer(game_id) VALUES ((SELECT id FROM room))
            """

    except:
        print("Ошибка в поиске или создании лобби")
    close_connection(connection)