import json

from aiogram import types

from keyboards.inline.blackjack_menu.blackjacj_endgame_menu import blackjack_endgame_menu
from keyboards.inline.blackjack_menu.blackjack_menu import blackjack_menu
from loader import bot
from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.statistics.statistics_repo import StatisticsRepo
from utils.db_api.user.user_repo import UserRepo


async def start_blackjack(game_id):
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    user_repo = UserRepo(conn=conn)

    deck = await repo.make_decks()
    await repo.update_deck(deck)

    players = await repo.get_players_list_to_announce(game_id)
    players_hands = [[], []]
    users_data = [[], []]
    i = 0
    for player in players:
        users_data[i] = await user_repo.get_user(players[i][0])
        i += 1

    await repo.give_first_cards(deck, players_hands[0], players_hands[1])
    await repo.set_deck(game_id=game_id, deck=deck)

    i = 0
    for player in players:
        await bot.send_message(player[2], parse_mode=types.ParseMode.HTML, text=
        f"Игра начинается!\n"
        f"Игрок 1: {users_data[0][1]} - @{users_data[0][2]}\n"
        f"Игрок 2: {users_data[1][1]} - @{users_data[1][2]}\n")
        await repo.set_players_hand(game_id, players[i][0], players_hands[i])
        msg = await bot.send_message(player[2], parse_mode=types.ParseMode.HTML, text=
        f"Каждый игрок получил по 2 карты!\n"
        f"Ваша рука: {players_hands[i]}, количество очков: {await repo.total_up(players_hands[i])}\n\n"
        f"Хотите взять ещё карту?", reply_markup=blackjack_menu)
        await repo.set_player_message_id(users_data[i][0], game_id, msg.message_id)
        i += 1
    await conn.close()

async def blackjack_endgame(game_id):
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    user_repo = UserRepo(conn=conn)
    stat_repo = StatisticsRepo(conn=conn)
    deposit_repo = DepositRepo(conn=conn)

    users_data = [[], []]
    rate = await repo.get_rate(game_id)
    players_hands_before = await repo.get_players_hands(game_id=game_id)
    players_hands = [[], []]
    i = 0
    for hand in players_hands_before:
        players_hands[i] = json.loads(hand[0])
        i += 1

    players = await repo.get_players_list_to_announce(game_id)
    result = await repo.compare_players_hands(players_hands[0], players_hands[1])

    i = 0
    for player in players:
        users_data[i] = await user_repo.get_user(players[i][0])
        i += 1

    await repo.set_result(game_id, result)
    if result == 'player_one_won':
        result = f'Победа игрока {users_data[0][1]} - @{users_data[0][2]}'
        await deposit_repo.plus_user_deposit(users_data[0][0], rate[0])
        await deposit_repo.minus_user_deposit(users_data[1][0], rate[0])
        await stat_repo.update_win_blackjack(users_data[0][0])
        await stat_repo.update_games_blackjack(users_data[0][0])
        await stat_repo.update_games_blackjack(users_data[1][0])
    elif result == 'player_two_won':
        result = f'Победа игрока {users_data[1][1]} - @{users_data[1][2]}'
        await deposit_repo.minus_user_deposit(users_data[0][0], rate[0])
        await deposit_repo.plus_user_deposit(users_data[1][0], rate[0])
        await stat_repo.update_win_blackjack(users_data[1][0])
        await stat_repo.update_games_blackjack(users_data[0][0])
        await stat_repo.update_games_blackjack(users_data[1][0])
    elif result == 'draw':
        result = 'Нет победителя'


    i = 0
    for player in players:
        msg = await repo.get_player_message_id(players[i][0], game_id)
        chat_id = await repo.get_player_chat_id(players[i][0], game_id)

        await repo.set_players_hand(game_id, players[i][0], players_hands[i])
        await bot.edit_message_text(message_id=int(msg[0]), chat_id=chat_id[0], parse_mode=types.ParseMode.HTML, text=
        f"Игра окончена!\n\n"
        f"Рука {users_data[0][1]} - @{users_data[0][2]}: {players_hands[0]} - {await repo.total_up(players_hands[0])}\n"
        f"Рука игрока {users_data[1][1]} - @{users_data[1][2]}: {players_hands[1]} - {await repo.total_up(players_hands[1])}\n\n"
        f"Результат: {result}.", reply_markup=blackjack_endgame_menu)
        i += 1
    await conn.close()
