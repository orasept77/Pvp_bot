import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.blackjack.blackjack import blackjack_endgame, player_make_turn
from keyboards.inline.blackjack_menu.blackjack_menu import blackjack_menu
from keyboards.inline.callback_datas import blackjack_callback
from loader import dp, scheduler
from shedulers.timers_sheduler import TimerRepository
from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.user.user_repo import UserRepo


@dp.callback_query_handler(blackjack_callback.filter(what_to_do="more"))
async def bot_blackjack_give_one_card(call:CallbackQuery, callback_data: dict, state: FSMContext):
    conn = await create_conn()
    repo = BlackJackRepo(conn=conn, scheduler=scheduler)
    user_repo = UserRepo(conn=conn)

    data = await state.get_data()
    game_id = await repo.get_player_game_id(call.from_user.id)
    await state.update_data(game_id=game_id[0])
    player_turn = await repo.get_player_turn(game_id[0])

    timer = TimerRepository(scheduler=scheduler, timer_name="blackjack", user_id=call.from_user.id, game_id=game_id[0])
    if call.from_user.id == player_turn['user_turn']:
        data = await state.get_data()
        await player_make_turn(game_id=data.get('game_id'), action="one_card", player_id=call.from_user.id, scheduler=scheduler)
        # player_turn_data = await user_repo.get_user(new_id)
        # deck = await repo.get_deck(data.get('game_id'))
        # deck = json.loads(deck[0])
        #
        # player_hand = await repo.get_player_hand(data.get('game_id'), call.from_user.id)
        # player_hand = json.loads(player_hand[0])
        #
        # await repo.give_card(deck, player_hand)
        # await repo.set_deck(data.get('game_id'), deck)
        # await repo.set_players_hand(data.get('game_id'), call.from_user.id, player_hand)
        # await repo.set_player_state(data.get('game_id'), call.from_user.id, 'MORE')
        #
        # msg = await repo.get_player_message_id(call.from_user.id, data.get('game_id'))
        # chat_id = await repo.get_player_chat_id(call.from_user.id, data.get('game_id'))
        # await call.bot.edit_message_text(message_id=msg[0], chat_id=chat_id[0], text=
        # f"Вы взяли ещё одну карту.\n\n"
        # f"Сейчас ход <b>{player_turn_data['custom_nick']}</b>\n\n"
        # f"Ваша рука: {player_hand} - {await repo.total_up(player_hand)}",
        #                                  parse_mode=types.ParseMode.HTML, reply_markup=blackjack_menu)
    else:
        await timer.pause_timer()
        await call.answer("Сейчас не ваш ход.", show_alert=True)
    await conn.close()

@dp.callback_query_handler(blackjack_callback.filter(what_to_do="stop"))
async def bot_blackjack_stop_taking(call:CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()

    conn = await create_conn()
    repo = BlackJackRepo(conn=conn, scheduler=scheduler)
    user_repo = UserRepo(conn=conn)

    if not data.get('game_id'):
        game_id = await repo.get_player_game_id(call.from_user.id)
        await state.update_data(game_id=game_id[0])


    data = await state.get_data()
    timer = TimerRepository(scheduler=scheduler, timer_name="blackjack", user_id=call.from_user.id, game_id=data.get('game_id'))

    await state.update_data(game_id=data.get('game_id'))
    player_turn = await repo.get_player_turn(data.get('game_id'))
    player_turn_data = await user_repo.get_user(player_turn['user_turn'])
    if call.from_user.id == player_turn['user_turn']:
        await player_make_turn(game_id=data.get('game_id'), action="stop_taking", player_id=call.from_user.id, scheduler=scheduler)
        #
        # await repo.set_player_state(data.get('game_id'), call.from_user.id, 'STOP')
        #
        # player_hand = await repo.get_player_hand(data.get('game_id'), call.from_user.id)
        # player_hand = json.loads(player_hand[0])
        #
        # states = await repo.get_players_states(data.get('game_id'))
        # if states[0][0] == 'STOP' and states[1][0] == 'STOP':
        #     await blackjack_endgame(data.get('game_id'), scheduler=scheduler)
        # else:
        #     msg = await repo.get_player_message_id(call.from_user.id, data.get('game_id'))
        #     chat_id = await repo.get_player_chat_id(call.from_user.id, data.get('game_id'))
        #     await call.bot.edit_message_text(message_id=msg[0], chat_id=chat_id[0], text=
        #         f"Вы решили больше не брать карт. Ожидаем конца хода второго игрока.\n\n"
        #         f"Ваша рука: {player_hand} - {await repo.total_up(player_hand)}",
        #         parse_mode=types.ParseMode.HTML)
    else:
        await call.answer("Сейчас не ваш ход.", show_alert=True)
    await conn.close()