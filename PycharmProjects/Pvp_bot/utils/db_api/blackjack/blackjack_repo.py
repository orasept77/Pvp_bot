from psycopg2._psycopg import cursor
from asyncpg.connection import Connection

from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query, fetchall_query, print_query, fetchone_query, mogrify_query

class BlackJackRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_players_list_to_announce(game_id):
        get_data_query = f"""
            SELECT * FROM blackjack_game_user WHERE game_id = {game_id}
        """
        connection = db_connection()
        try:
            return fetchall_query(connection, get_data_query)
        except:
            print("Ошибка анонса игроков.")
        close_connection(connection)


    async def set_players_hand(game_id, user_id, hand):
        query = f"""
        UPDATE blackjack_game_user SET hand = '{hand}' WHERE game_id = {game_id} AND user_id = {user_id}
        """
        connection = db_connection()
        try:
            return execute_query(connection, query)
        except:
            print("Ошибка записи руки игрока..")
        close_connection(connection)


# def set_dealer_hand(game_id, hand, deck):
#     query = "UPDATE blackjack_game_dealer SET hand = %s, deck = %s WHERE game_id = {}".format(game_id)
#     print(query)
#     connection = db_connection()
#     connection.autocommit = True
#     try:
#         return print(cursor.mogrify(query, (hand, deck)))
#         #return mogrify_query(connection, query, hand, deck)
#     except:
#         print("Ошибка записи руки диллера.")
#     close_connection(connection)


    async def set_dealer_hand(self, game_id, hand, deck):
        sql = 'UPDATE blackjack_game_dealer SET hand = $1, deck = $2 WHERE game_id = $3'
        res = await self.conn.fetch(sql, game_id, hand, deck)
        return res