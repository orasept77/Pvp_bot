from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.blackjack.blackjack import start_blackjack
from keyboards.inline.callback_datas import create_lobby_callback, leave_lobby_callback, blackjack_endgame_callback

from keyboards.inline.choose_game_menu.leave_lobby import leave_lobby_menu
from loader import dp
from states.start_game import StartGame_State

from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn


"""@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="blackjack"),
                           state=StartGame_State.game)"""

@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="blackjack"))
async def bot_blackjack_create_lobby(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()

    if data.get('game_id'):
        await repo.delete_game_blackjack(data.get('game_id'))
        await state.update_data(game_id=None)
        data = await state.get_data()

    await state.update_data(chat_id=call.message.chat.id)
    game_start = await repo.find_lobby_blackjack(data.get('user_id'), data.get('id'), data.get('chat_id'))

    await call.message.answer(
        f"Вы добавленны в лобби. Поиск игроков...\n",
        parse_mode=types.ParseMode.HTML, reply_markup=leave_lobby_menu)
    if game_start:
        await start_blackjack(game_start)



@dp.callback_query_handler(blackjack_endgame_callback.filter(result="revenge"))
async def bot_blackjack_revenge(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    await repo.set_player_state(data.get('game_id'), data.get('user_id'), 'REVENGE')

    states = await repo.get_players_states(data.get('game_id'))
    if states[0][0] == 'REVENGE' and states[1][0] == 'REVENGE' and states != None:
        await call.message.answer(
            f"Вы приняли предложение реванша.\n",
            parse_mode=types.ParseMode.HTML)
        await repo.create_revenge_game(data.get('game_id'))
        await start_blackjack(data.get('game_id'))
    else:
        await call.message.answer(
            f"Вы отправили предложение реванша.\n",
            parse_mode=types.ParseMode.HTML, )


@dp.callback_query_handler(blackjack_endgame_callback.filter(result="revenge"))
async def bot_blackjack_revenge_cancel(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    await repo.delete_game_blackjack(data.get('game_id'))

    await call.message.answer(
        f"Вы отменили предложение реванша.\n"
        f"Для доступа к меню используйте команду /start",
        parse_mode=types.ParseMode.HTML)
    await state.finish()

@dp.callback_query_handler(leave_lobby_callback.filter(leave="yes"))
async def bot_blackjack_lobby_leave(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)

    data = await state.get_data()
    await repo.delete_lobby_blackjack(data.get('user_id'))
    await call.message.answer(
        f"Вы отменили поиск игры.\n"
        f"Для доступа к меню используйте команду /start.",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(blackjack_endgame_callback.filter(result="leave"))
async def bot_blackjack_game_leave(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()

    await repo.delete_game_blackjack(data.get('game_id'))
    await state.update_data(game_id=None)

    await call.message.answer(
        f"Вы покинули игру.\n"
        f"Для доступа к меню используйте команду /start.",
        parse_mode=types.ParseMode.HTML)
    await state.finish()
