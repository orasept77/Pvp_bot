import json

from asyncpg.connection import Connection

import numpy as np
import random


class BlackJackRepo:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.deck = []
        self.card_types = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'B', 'D', 'K']
        self.blackjack = set(['A', 10])

    async def update_deck(self, deck):
        self.deck = deck

    # Создание колоды
    async def make_decks(self):
        new_deck = []
        for j in range(4):
            new_deck.extend(self.card_types)
        random.shuffle(new_deck)
        return new_deck

    # Эта функция перечисляет все комбинации значений туза в
    # массив sum_array.
    # Например, если у вас 2 туза, есть 4 комбинации:
    # [[1,1], [1,11], [11,1], [11,11]]
    # Эти комбинации приводят к 3 уникальным суммам: [2, 12, 22]
    # Из этих 3 только 2 являются <= 21, поэтому они возвращаются: [2, 12]+
    async def get_ace_values(self, temp_list):
        sum_array = np.zeros((2 ** len(temp_list), len(temp_list)))
        # Этот цикл получает комбинации
        for i in range(len(temp_list)):
            n = len(temp_list) - i
            half_len = int(2 ** n * 0.5)
            for rep in range(int(sum_array.shape[0] / half_len / 2)):
                sum_array[rep * 2 ** n: rep * 2 ** n + half_len, i] = 1
                sum_array[rep * 2 ** n + half_len: rep * 2 ** n + half_len * 2, i] = 11
                # Только значения, которые подходят (<=21)
        return list(set([int(s) for s in np.sum(sum_array, axis=1) \
                         if s <= 21]))  # Конвертация num_aces, int в list

    # Например, если num_aces = 2, вывод должен быть [[1,11],[1,11]]
    # Нужен этот формат для функции get_ace_values
    async def ace_values(self, num_aces):
        temp_list = []
        for i in range(num_aces):
            temp_list.append([1, 11])
        return await self.get_ace_values(temp_list)

    # Сумма на руках
    async def total_up(self, hand):
        aces = 0
        total = 0

        original_hand = hand
        replaced_hand = []
        for item in original_hand:
            if item == 'A':
                replaced_hand.append(item)
            elif item == 'B' or item == 'D' or item == 'K':
                replaced_hand.append(10)
            else:
                replaced_hand.append(item)

        for card in replaced_hand:
            if card != 'A':
                total += card
            else:
                aces += 1

        # Вызовите функцию ace_values, чтобы получить список возможных значений для тузов на руках.
        ace_value_list = await self.ace_values(aces)
        final_totals = [i + total for i in ace_value_list if i + total <= 21]

        if final_totals == []:
            return min(ace_value_list) + total
        else:
            return max(final_totals)

    async def empty_hand(self):
        return []

    # Выдать карту игроку
    async def give_card(self, deck, hand):
        hand.append(deck.pop(0))

    # Получение первых двух карт
    async def give_first_cards(self, deck, player_one_hand, player_two_hand):
        # Получение ПЕРВОЙ карты
        await self.give_card(deck, player_one_hand)
        await self.give_card(deck, player_two_hand)
        # Получение ВТОРОЙ карты
        await self.give_card(deck, player_one_hand)
        await self.give_card(deck, player_two_hand)

    # Проверка руки на блекджек
    async def check_blackjack(self, hand):
        if set(hand) == self.blackjack:
            return True

    # Проверка на перебор (больше 21 очка в руке)
    async def more_than_21(self, hand):
        if await self.total_up(hand) > 21:
            return True

    # Сравнение рук игроков
    async def compare_players_hands(self, player_one_hand, player_two_hand):
        if await self.total_up(player_one_hand) > await self.total_up(player_two_hand) and await self.total_up(player_one_hand) <= 21:
            #print('у игрока 1 <= 21, и при этом у игрока 1 > чем у игрока 2')
            return 'player_one_won'
        elif await self.total_up(player_one_hand) < await self.total_up(player_two_hand) and await self.total_up(player_two_hand) <= 21:
            #print('у игрока 2 <= 21, и при этом у игрока 1 > чем у игрока 2')
            return 'player_two_won'
        elif await self.total_up(player_one_hand) == await self.total_up(player_two_hand) and await self.total_up(player_one_hand) <= 21:
            #print('у игроков одинаковое количество очков и меньше 21го')
            return 'draw'
        elif await self.total_up(player_one_hand) == await self.total_up(player_two_hand) and await self.more_than_21(player_one_hand):
            #print('у игроков одинаковое количество очков и больше 21го')
            return 'draw'
        elif await self.more_than_21(player_one_hand) and not await self.more_than_21(player_two_hand):
            #print('у игрока 1 > 21, а игрока 2 < 21')
            return 'player_two_won'
        elif await self.more_than_21(player_two_hand) and not await self.more_than_21(player_one_hand):
            #print('у игрока 2 > 21, а игрока 1 < 21')
            return 'player_one_won'
        elif await self.more_than_21(player_two_hand) and await self.more_than_21(player_one_hand):
            #print('у обоих больше 21')
            return 'draw'
        else:
            #print(await self.total_up(player_one_hand), await self.more_than_21(player_one_hand))
            #print(await self.total_up(player_two_hand), await self.more_than_21(player_one_hand))
            #print('UNEXPECTED_RESULT')
            return 'UNEXPECTED_RESULT'

    async def find_lobby_blackjack(self, user_id, rates_id, chat_id):
        find_lobby_query = 'SELECT * FROM blackjack_lobby WHERE rates_id = $1'
        create_lobby_query = 'INSERT INTO blackjack_lobby (user_id, rates_id, chat_id) VALUES ($1, $2, $3)'
        create_game_query = """
        WITH game AS (
            INSERT INTO blackjack_game(rates_id) VALUES ($1)
            RETURNING id
        )
            SELECT id FROM game
        """
        connect_players_to_game_query_one = 'INSERT INTO blackjack_game_user(user_id, game_id, chat_id) VALUES ($1, $2, $3);'
        connect_players_to_game_query_two = 'INSERT INTO blackjack_game_user(user_id, game_id, chat_id) VALUES ($1, $2, $3);'
        find_lobby_result = await self.conn.fetchrow(find_lobby_query, int(rates_id))
        if not find_lobby_result:
            return await self.conn.fetch(create_lobby_query, int(user_id), int(rates_id), int(chat_id))
        else:
            game = await self.conn.fetch(create_game_query, int(rates_id))
            game_id = game[0][0]
            await self.conn.fetch(connect_players_to_game_query_one, int(user_id), int(game_id), int(chat_id))
            await self.conn.fetch(connect_players_to_game_query_two, int(find_lobby_result[0]), int(game_id), int(find_lobby_result[2]))
            await self.delete_lobby_blackjack(find_lobby_result[0])
            return game_id

    async def start_invite_game(self, user_id, chat_id, lobby_id):
        find_lobby_query = 'SELECT * FROM blackjack_invite_lobby WHERE id = $1'
        create_game_query = """
        WITH game AS (
            INSERT INTO blackjack_game(rates_id) VALUES ($1)
            RETURNING id
        )
            SELECT id FROM game
        """
        connect_players_to_game_query_one = 'INSERT INTO blackjack_game_user(user_id, game_id, chat_id) VALUES ($1, $2, $3);'
        connect_players_to_game_query_two = 'INSERT INTO blackjack_game_user(user_id, game_id, chat_id) VALUES ($1, $2, $3);'

        find_lobby_result = await self.conn.fetchrow(find_lobby_query, int(lobby_id))
        rates_id = int(find_lobby_result[2])

        game = await self.conn.fetch(create_game_query, int(rates_id))
        game_id = game[0][0]

        await self.conn.fetch(create_game_query, rates_id)
        await self.conn.fetch(connect_players_to_game_query_one, int(user_id), int(game_id), int(chat_id))
        await self.conn.fetch(connect_players_to_game_query_two, int(find_lobby_result[1]), int(game_id), int(find_lobby_result[3]))
        await self.delete_lobby_blackjack(find_lobby_result[0])
        return game_id

    async def create_invite_lobby(self, user_id, rates_id, game_id):
        sql = "INSERT INTO blackjack_invite_lobby (user_id, rates_id, chat_id) VALUES ($1, $2, $3)"
        res = await self.conn.fetch(sql, user_id, int(rates_id), int(game_id))
        return res

    async def get_invite_lobby_id(self, user_id):
        sql = "SELECT id FROM blackjack_invite_lobby WHERE user_id = $1"
        res = await self.conn.fetch(sql, user_id)
        return res

    async def delete_invite_lobby_by_id(self, id):
        sql = "DELETE FROM blackjack_invite_lobby WHERE id = $1"
        res = await self.conn.fetch(sql, id)
        return res

    async def delete_invite_lobby_by_userid(self, user_id):
        sql = "DELETE FROM blackjack_invite_lobby WHERE user_id = $1"
        res = await self.conn.fetch(sql, user_id)
        return res

    async def create_revenge_game(self, game_id):
        sql = "UPDATE blackjack_game SET result = 'REVENGE', deck = '[]', game_round = game_round + 1 WHERE id = $1;"
        await self.conn.fetch(sql, game_id)
        sql = "UPDATE blackjack_game_user SET hand = '[]', state = 'REVENGE' WHERE game_id = $1;"
        res = await self.conn.fetch(sql, game_id)
        return res

    async def set_player_message_id(self, user_id, game_id, message_id):
        sql = 'UPDATE blackjack_game_user SET message_id = $3 WHERE user_id = $1 AND game_id = $2'
        res = await self.conn.fetchrow(sql, user_id, game_id, message_id)
        return res

    async def get_player_message_id(self, user_id, game_id):
        sql = 'SELECT message_id FROM blackjack_game_user WHERE user_id = $1 AND game_id = $2'
        res = await self.conn.fetchrow(sql, user_id, game_id)
        return res

    async def set_player_chat_id(self, user_id, game_id, message_id):
        sql = 'UPDATE blackjack_game_user SET chat_id = $3 WHERE user_id = $1 AND game_id = $2'
        res = await self.conn.fetchrow(sql, user_id, game_id, message_id)
        return res

    async def get_player_chat_id(self, user_id, game_id):
        sql = 'SELECT chat_id FROM blackjack_game_user WHERE user_id = $1 AND game_id = $2'
        res = await self.conn.fetchrow(sql, user_id, game_id)
        return res

    async def get_player_game_id(self, user_id):
        sql = 'SELECT game_id FROM blackjack_game_user WHERE user_id = $1'
        res = await self.conn.fetchrow(sql, user_id)
        return res

    async def get_players_list_to_announce(self, game_id):
        sql = 'SELECT * FROM blackjack_game_user WHERE game_id = $1'
        res = await self.conn.fetch(sql, game_id)
        return res

    async def set_player_state(self, game_id, user_id, state):
        sql = 'UPDATE blackjack_game_user SET state = $1 WHERE game_id = $2 AND user_id = $3'
        res = await self.conn.fetch(sql, state, game_id, user_id)
        return res

    async def get_players_states(self, game_id):
        sql = 'SELECT state FROM blackjack_game_user WHERE game_id = $1'
        res = await self.conn.fetch(sql, game_id)
        return res

    async def set_players_hand(self, game_id, user_id, hand):
        sql = 'UPDATE blackjack_game_user SET hand = $1 WHERE game_id = $2 AND user_id = $3'
        res = await self.conn.fetch(sql, json.dumps(hand), game_id, user_id)
        return res

    async def set_deck(self, game_id, deck):
        sql = 'UPDATE blackjack_game SET deck = $1 WHERE id = $2'
        res = await self.conn.fetch(sql, json.dumps(deck), game_id)
        return res

    async def get_player_hand(self, game_id, user_id):
        sql = 'SELECT hand FROM blackjack_game_user WHERE game_id = $1 AND user_id = $2'
        res = await self.conn.fetchrow(sql, game_id, user_id)
        return res

    async def get_players_hands(self, game_id):
        sql = 'SELECT hand FROM blackjack_game_user WHERE game_id = $1'
        res = await self.conn.fetch(sql, game_id)
        return res

    async def get_deck(self, game_id):
        sql = 'SELECT deck FROM blackjack_game WHERE id = $1'
        res = await self.conn.fetchrow(sql, game_id)
        return res

    async def set_result(self, game_id, result):
        sql = 'UPDATE blackjack_game SET result = $1 WHERE id = $2'
        res = await self.conn.fetchrow(sql, result, game_id)
        return res

    async def get_rate(self, game_id):
        sql = 'SELECT r.value FROM blackjack_game as bj LEFT JOIN rates AS r ON bj.rates_id=r.id WHERE bj.id=$1'
        res = await self.conn.fetchrow(sql, game_id)
        return res

    async def delete_lobby_blackjack(self, user_id):
        sql = 'DELETE FROM blackjack_lobby WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def delete_game_blackjack(self, game_id):
        sql = 'DELETE FROM blackjack_game_user WHERE game_id = $1;'
        await self.conn.fetch(sql, game_id)
        sql = 'DELETE FROM blackjack_game WHERE id = $1;'
        res = await self.conn.fetch(sql, game_id)
        return res
