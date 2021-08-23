import json

from aiogram import types

from keyboards.inline.blackjack_menu.blackjacj_endgame_menu import blackjack_endgame_menu
from keyboards.inline.blackjack_menu.blackjack_menu import blackjack_menu
from loader import bot
from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn


async def start_blackjack(game_id):
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)

    deck = await repo.make_decks()
    await repo.update_deck(deck)

    players = await repo.get_players_list_to_announce(game_id)
    players_hands = [[], []]
    dealer_hand = []
    await repo.give_first_cards(deck, players_hands[0], players_hands[1], dealer_hand)
    await repo.set_dealer_hand(game_id=game_id, hand=dealer_hand)
    await repo.set_deck(game_id=game_id, deck=deck)

    i = 0
    for player in players:
        await bot.send_message(player[2], parse_mode=types.ParseMode.HTML, text=
        f"Игра начинается!\n")
        await repo.set_players_hand(game_id, players[i][0], players_hands[i])
        await bot.send_message(player[2], parse_mode=types.ParseMode.HTML, text=
        f"Каждый игрок получил по 2 карты!\n"
        f"Ваша рука: {players_hands[i]}, количество очков: {await repo.total_up(players_hands[i])}\n\n"
        f"Хотите взять ещё карту?", reply_markup=blackjack_menu)
        i += 1
    await conn.close()

async def blackjack_endgame(game_id):
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)

    dealer_hand = await repo.get_dealer_hand(game_id=game_id)
    players_hands_before = await repo.get_players_hands(game_id=game_id)
    players_hands = [[], []]
    deck = await repo.get_deck(game_id=game_id)
    i = 0
    for hand in players_hands_before:
        players_hands[i] = json.loads(hand[0])
        i += 1
    deck = json.loads(deck[0])
    dealer_hand = json.loads(dealer_hand[0])

    await repo.dealer_take_card_if_totalup_less_17(deck, dealer_hand)
    players = await repo.get_players_list_to_announce(game_id)
    result = await repo.compare_players_hands(players_hands[0], players_hands[1])

    result = await repo.compare_players_with_dealer_hands(dealer_hand, players_hands[0], players_hands[1], result)
    await repo.set_result(game_id, result)
    if result == 'player_one_won':
        result = 'Победа игрока 1'
    elif result == 'player_two_won':
        result = 'Победа игрока 2'
    elif result == 'dealer_won':
        result = 'Победа дилера'
    elif result == 'draw':
        result = 'Нет победителя'

    i = 0
    for player in players:
        await bot.send_message(player[2], parse_mode=types.ParseMode.HTML, text=
        f"Дилер добирает карты.\n")
        await repo.set_players_hand(game_id, players[i][0], players_hands[i])
        await bot.send_message(player[2], parse_mode=types.ParseMode.HTML, text=
        f"Игра окончена!\n\n"
        f"Рука дилера: {dealer_hand} - {await repo.total_up(dealer_hand)}\n"
        f"Рука игрока 1: {players_hands[0]} - {await repo.total_up(players_hands[0])}\n"
        f"Рука игрока 2: {players_hands[1]} - {await repo.total_up(players_hands[1])}\n\n"
        f"Результат: {result}.", reply_markup=blackjack_endgame_menu)
        i += 1
    conn.close()
