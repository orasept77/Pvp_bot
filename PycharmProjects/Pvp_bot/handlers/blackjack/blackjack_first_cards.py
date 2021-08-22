import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.blackjack.blackjack import blackjack_endgame
from keyboards.inline.blackjack_menu import blackjack_menu
from keyboards.inline.callback_datas import blackjack_callback

from loader import dp
from states.start_game import StartGame_State
from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn


@dp.callback_query_handler(blackjack_callback.filter(what_to_do="more"),
                           state=StartGame_State.game)
async def bot_blackjack_give_one_card(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    if not data.get('game_id'):
        game_id = await repo.get_player_game_id(data.get('user_id'))
        await state.update_data(game_id=game_id[0])

    data = await state.get_data()
    deck = await repo.get_deck(data.get('game_id'))
    deck = json.loads(deck[0])

    player_hand = await repo.get_player_hand(data.get('game_id'), data.get('user_id'))
    player_hand = json.loads(player_hand[0])
    await repo.give_card(deck, player_hand)
    await repo.set_deck(data.get('game_id'), deck)
    await repo.set_players_hand(data.get('game_id'), data.get('user_id'), player_hand)
    await repo.set_player_state(data.get('game_id'), data.get('user_id'), 'MORE')
    await call.message.answer(
        f"Вы взяли ещё одну карту.\n\n"
        f"Ваша рука: {player_hand} - {await repo.total_up(player_hand)}",
        parse_mode=types.ParseMode.HTML, reply_markup=blackjack_menu)

    await StartGame_State.game.set()


@dp.callback_query_handler(blackjack_callback.filter(what_to_do="stop"),
                           state=StartGame_State.game)
async def bot_blackjack_stop_taking(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)

    if not data.get('game_id'):
        game_id = await repo.get_player_game_id(data.get('user_id'))
        await state.update_data(game_id=game_id[0])

    data = await state.get_data()
    await repo.set_player_state(data.get('game_id'), data.get('user_id'), 'STOP')

    player_hand = await repo.get_player_hand(data.get('game_id'), data.get('user_id'))
    player_hand = json.loads(player_hand[0])

    states = await repo.get_players_states(data.get('game_id'))
    if states[0][0] == 'STOP' and states[1][0] == 'STOP':
        await blackjack_endgame(data.get('game_id'))
    else:
        await call.message.answer(
            f"Вы решили больше не брать карт. Ожидаем конца хода второго игрока.\n\n"
            f"Ваша рука: {player_hand} - {await repo.total_up(player_hand)}",
            parse_mode=types.ParseMode.HTML)
    await StartGame_State.game.set()
