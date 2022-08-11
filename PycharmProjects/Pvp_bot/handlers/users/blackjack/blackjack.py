import json

import random
from aiogram import types

from data.config import BLACKJACK_IS_DEALER_ENABLED
from keyboards.inline.blackjack_menu.blackjacj_endgame_menu import blackjack_endgame_menu
from keyboards.inline.blackjack_menu.blackjack_menu import blackjack_menu
from loader import bot

from shedulers.timers_sheduler import TimerRepository
from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.statistics.statistics_repo import StatisticsRepo
from utils.db_api.user.user_repo import UserRepo


async def start_blackjack(game_id, scheduler):
    conn = await create_conn()
    repo = BlackJackRepo(conn=conn, scheduler=scheduler)
    user_repo = UserRepo(conn=conn)

    deck = await repo.make_decks()
    await repo.update_deck(deck)

    players = await repo.get_players_list_to_announce(game_id)
    players_hands = [[], []]
    dealer_hand = []
    await repo.give_card(deck, dealer_hand)
    await repo.give_card(deck, dealer_hand)
    await repo.set_dealer_hand(game_id=game_id, hand=dealer_hand)
    player_timers = [[], []]
    users_data = []
    i = 0
    for player in players:
        users_data.append(await user_repo.get_user(players[i][0]))
        i += 1

    await repo.give_first_cards(deck, players_hands[0], players_hands[1])

    await repo.set_deck(game_id=game_id, deck=deck)

    player_turn = random.choice(users_data)
    player_turn_id = player_turn['id']
    await repo.set_player_turn(game_id, player_turn_id)

    meet_msg = f"Игра начинается!\n"\
        f"Игрок 1: {users_data[0]['custom_nick']}\n"\
        f"Игрок 2: {users_data[1]['custom_nick']}\n\n"

    if BLACKJACK_IS_DEALER_ENABLED is True:
        await repo.give_card(deck, dealer_hand)
        await repo.give_card(deck, dealer_hand)
        await repo.set_dealer_hand(game_id, dealer_hand)
        meet_msg += "Вы так-же играете против дилера."

    i = 0
    for player in players:
        player_timers[i] = TimerRepository(scheduler=scheduler, timer_name="blackjack", user_id=player['user_id'], game_id=game_id)
        await player_timers[i].start_timer()
        if player['user_id'] != player_turn_id:
            await player_timers[i].pause_timer()
        else:
            await player_timers[i].update_timer()
        await bot.send_message(player['user_id'], parse_mode=types.ParseMode.HTML, text=meet_msg)
        await repo.set_players_hand(game_id, players[i]['user_id'], players_hands[i])
        msg = await bot.send_message(player['user_id'], parse_mode=types.ParseMode.HTML, text=
        f"Каждый игрок получил по 2 карты!\n\n"
        f"<b>Первым ходит: {player_turn['custom_nick']}</b>\n\n"
        f"Ваша рука: <b>{players_hands[i]}</b>, количество очков: <b>{await repo.total_up(players_hands[i])}</b>\n\n"
        f"Хотите взять ещё карту?", reply_markup=blackjack_menu)
        await repo.set_player_message_id(users_data[i]['id'], game_id, msg.message_id)
        i += 1
    await conn.close()

async def player_make_turn(game_id, action, player_id, scheduler):
    conn = await create_conn()
    repo = BlackJackRepo(conn=conn, scheduler=scheduler)
    user_repo = UserRepo(conn=conn)

    player_timers = [[], []]

    players = await repo.get_players_list_to_announce(game_id)
    player_turn = await repo.get_player_turn(game_id)
    player_turn_id = player_turn['user_turn']
    player_turn_id_new = player_turn_id
    i = 0
    for player in players:
        player_state = await repo.get_player_states(game_id, player['user_id'])
        if player['user_id'] != player_turn_id:
            if player_state['state'] != 'STOP':
                player_turn_id_new = player['user_id']
        i += 1

    await repo.set_player_turn(game_id, player_turn_id_new)
    player_turn_data = await user_repo.get_user(player_turn_id_new)
    message_turn = f"<b>Ход игрока: {player_turn_data['custom_nick']}</b>\n\n"

    if action == 'one_card':

        deck = await repo.get_deck(game_id)
        deck = json.loads(deck[0])
        player_hand = await repo.get_player_hand(game_id, player_id)
        player_hand = json.loads(player_hand[0])
        await repo.give_card(deck, player_hand)
        await repo.set_deck(game_id, deck)
        await repo.set_players_hand(game_id, player_id, player_hand)
        await repo.set_player_state(game_id, player_id, 'MORE')

        i = 0
        for player in players:
            player_state = await repo.get_player_states(game_id, player['user_id'])
            player_timers[i] = TimerRepository(scheduler=scheduler, timer_name="blackjack", user_id=player['user_id'],
                                               game_id=game_id)
            if player['user_id'] == player_turn_id:
                if player_state['state'] != 'STOP':
                    await player_timers[i].update_timer()
                else:
                    await player_timers[i].pause_timer()
            else:
                if player_state['state'] != 'STOP':
                    await player_timers[i].update_timer()
                else:
                    pass

            if player['user_id'] == player_turn_id:
                message_for_user = message_turn + 'Вы решили взять дополнительную карту.\n' \
                                                  f'Ваша рука: <b>{player_hand}</b> - <b>{await repo.total_up(player_hand)}</b>\n\n'
            else:
                second_player_hand = await repo.get_player_hand(game_id, player['user_id'])
                second_player_hand = json.loads(second_player_hand[0])
                message_for_user = message_turn + f'Оппонент решил взять ещё одну карту.\nКарт в руке: <b>{str(len(player_hand))}</b>\n\n' \
                                                  f'Ваша рука: <b>{second_player_hand}</b> - <b>{await repo.total_up(second_player_hand)}</b>\n\n'
            chat_id = await repo.get_player_chat_id(player['user_id'], game_id)  # chat_id
            msg_id = await repo.get_player_message_id(player['user_id'], game_id)  # message_id
            await bot.edit_message_text(chat_id=chat_id['chat_id'], message_id=msg_id['message_id'],
                                        parse_mode=types.ParseMode.HTML, text=message_for_user,
                                        reply_markup=blackjack_menu)
            i += 1
    elif action == 'stop_taking':
        await repo.set_player_state(game_id, player_id, 'STOP')

        player_hand = await repo.get_player_hand(game_id, player_id)
        player_hand = json.loads(player_hand[0])

        states = await repo.get_players_states(game_id)
        if states[0][0] == 'STOP' and states[1][0] == 'STOP':
            await blackjack_endgame(game_id, scheduler=scheduler)
        else:
            i = 0
            for player in players:
                player_timers[i] = TimerRepository(scheduler=scheduler, timer_name="blackjack",
                                                   user_id=player['user_id'], game_id=game_id)
                if player['user_id'] == player_turn_id:
                    await player_timers[i].pause_timer()
                else:
                    await player_timers[i].update_timer()

                if player['user_id'] == player_turn_id:
                    message_for_user = message_turn + 'Вы решили больше не брать карт. Ожидаем конца хода оппонента.\n' \
                                                      f'Ваша рука: <b>{player_hand}</b> - <b>{await repo.total_up(player_hand)}</b>\n\n'
                else:
                    second_player_hand = await repo.get_player_hand(game_id, player['user_id'])
                    second_player_hand = json.loads(second_player_hand[0])
                    message_for_user = message_turn + f'Оппонент решил больше не брать карт.\nКарт в руке: <b>{str(len(player_hand))}</b>\n\n' \
                                                      f'Ваша рука: <b>{second_player_hand}</b> - <b>{await repo.total_up(second_player_hand)}\n\n</b>'
                chat_id = await repo.get_player_chat_id(player['user_id'], game_id)  # chat_id
                msg_id = await repo.get_player_message_id(player['user_id'], game_id)  # message_id
                await bot.edit_message_text(chat_id=chat_id['chat_id'], message_id=msg_id['message_id'],
                                            parse_mode=types.ParseMode.HTML, text=message_for_user,
                                            reply_markup=blackjack_menu)
                i += 1

async def blackjack_endgame(game_id, scheduler):
    conn = await create_conn()
    repo = BlackJackRepo(conn=conn, scheduler=scheduler)
    user_repo = UserRepo(conn=conn)
    stat_repo = StatisticsRepo(conn=conn)
    deposit_repo = DepositRepo(conn=conn)

    player_timers = [[], []]
    users_data = [[], []]

    rate = await repo.get_rate(game_id)
    deck = await repo.get_deck(game_id=game_id)
    if BLACKJACK_IS_DEALER_ENABLED is True:
        dealer_hand = await repo.get_dealer_hand(game_id=game_id)
        dealer_hand = json.loads(dealer_hand[0])
        await repo.dealer_take_card_if_totalup_less_17(deck, dealer_hand)
    players_hands_before = await repo.get_players_hands(game_id=game_id)
    players_hands = [[], []]
    i = 0
    for hand in players_hands_before:
        players_hands[i] = json.loads(hand[0])
        i += 1

    players = await repo.get_players_list_to_announce(game_id)
    result = await repo.compare_players_hands(players_hands[0], players_hands[1])
    if BLACKJACK_IS_DEALER_ENABLED is True:
        result = await repo.compare_players_with_dealer_hands(dealer_hand, players_hands[0], players_hands[1], result)

    i = 0
    for player in players:
        users_data[i] = await user_repo.get_user(players[i][0])
        i += 1

    await repo.set_result(game_id, result)
    if result == 'player_one_won':
        result = f"Победа игрока {users_data[0]['custom_nick']}"
        await deposit_repo.plus_user_deposit(users_data[0]["id"], rate["value"])
        await deposit_repo.minus_user_deposit(users_data[1]["id"], rate["value"])

        await stat_repo.update_win_balance(users_data[0]["id"], rate["value"])
        await stat_repo.update_lost_balance(users_data[1]["id"], rate["value"])

        await stat_repo.update_win_blackjack(users_data[0]["id"])
        await stat_repo.update_games_blackjack(users_data[0]["id"])
        await stat_repo.update_games_blackjack(users_data[1]["id"])
    elif result == 'player_two_won':
        result = f"Победа игрока {users_data[1]['custom_nick']}"
        await deposit_repo.minus_user_deposit(users_data[0]["id"], rate["value"])
        await deposit_repo.plus_user_deposit(users_data[1]["id"], rate["value"])

        await stat_repo.update_win_balance(users_data[1]["id"], rate["value"])
        await stat_repo.update_lost_balance(users_data[0]["id"], rate["value"])

        await stat_repo.update_win_blackjack(users_data[1]["id"])
        await stat_repo.update_games_blackjack(users_data[0]["id"])
        await stat_repo.update_games_blackjack(users_data[1]["id"])
    elif result == 'dealer_won':
        result = 'Победа дилера'
        await deposit_repo.minus_user_deposit(users_data[0]["id"], rate["value"])
        await deposit_repo.minus_user_deposit(users_data[1]["id"], rate["value"])
        await stat_repo.update_lost_balance(users_data[0]["id"], rate["value"])
        await stat_repo.update_lost_balance(users_data[1]["id"], rate["value"])
        await stat_repo.update_games_blackjack(users_data[0]["id"])
        await stat_repo.update_games_blackjack(users_data[1]["id"])
    elif result == 'draw':
        result = 'Нет победителя'


    i = 0
    player_timers = [[], []]
    for player in players:
        msg = await repo.get_player_message_id(players[i][0], game_id)
        chat_id = await repo.get_player_chat_id(players[i][0], game_id)
        player_timers[i] = TimerRepository(scheduler=scheduler, timer_name="blackjack", user_id=player['user_id'], game_id=game_id)
        await player_timers[i].remove_timer()
        await repo.set_players_hand(game_id, players[i][0], players_hands[i])
        if BLACKJACK_IS_DEALER_ENABLED is True:
            await bot.edit_message_text(message_id=int(msg[0]), chat_id=chat_id[0], parse_mode=types.ParseMode.HTML, text=
            f"Игра окончена!\n\n"
            f"Дилер добирает карты, если у него меньше 17.\n"
            f"Рука дилера после добора:\n"
            f"Рука <b>дилера</b>: <b>{dealer_hand}</b> - <b>{await repo.total_up(dealer_hand)}</b>\n\n"
            f"Рука <b>{users_data[0]['custom_nick']}</b>: <b>{players_hands[0]}</b> - <b>{await repo.total_up(players_hands[0])}</b>\n\n"
            f"Рука <b>{users_data[1]['custom_nick']}</b>: <b>{players_hands[1]}</b> - <b>{await repo.total_up(players_hands[1])}</b>\n\n"
            f"Результат: <b>{result}</b>.", reply_markup=blackjack_endgame_menu)
        else:
            await bot.edit_message_text(message_id=int(msg[0]), chat_id=chat_id[0], parse_mode=types.ParseMode.HTML,
            text=
            f"Игра окончена!\n\n"
            f"Рука <b>{users_data[0]['custom_nick']}</b>: <b>{players_hands[0]}</b> - <b>{await repo.total_up(players_hands[0])}</b>\n\n"
            f"Рука <b>{users_data[1]['custom_nick']}</b>: <b>{players_hands[1]}</b> - <b>{await repo.total_up(players_hands[1])}</b>\n\n"
            f"Результат: <b>{result}</b>.", reply_markup=blackjack_endgame_menu)
        i += 1
    await conn.close()
