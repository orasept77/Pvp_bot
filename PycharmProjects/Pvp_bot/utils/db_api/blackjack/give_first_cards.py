

from psycopg2._psycopg import cursor

from games.blackjack.game import empty_hand, give_first_cards
from games.blackjack.logic import make_decks
from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query, fetchall_query, print_query, fetchone_query


card_types = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
blackjack = set(['A', 10])

def give_first_cards_for_the_players(room_id):
    connection = db_connection()

    # Создание колоды и сброс рук
    deck = make_decks(1, card_types)
    dealer_hand = empty_hand()
    player_one_hand = empty_hand()
    player_two_hand = empty_hand()
    get_data_query = f"""
    SELECT bj.*, room.* FROM blackjacks as bj 
    LEFT JOIN rooms as room on bj.room_id=room.id
    WHERE room.id = {room_id}
    """
    give_first_cards(deck, player_one_hand, player_two_hand, dealer_hand)
    find_empty_room_to_connect_query = f"""
    
    """


    try:
        empty_room = None
        connect_to_the_empty_room_query = None
        try:
            empty_room = fetchone_query(connection, find_empty_room_to_connect_query)
            connect_to_the_empty_room_query = f"UPDATE rooms SET player_two = {user.id} WHERE rooms.id = {empty_room[8]}"
        except:
            pass
        if empty_room == None:
            # Создаём свободную комнату для подключения
            execute_query(connection, create_empty_room_query)
            print("Созданна новая комната для блекджека")
    except:
        print("Ошибка поиске комнаты для блекджека")
    close_connection(connection)
