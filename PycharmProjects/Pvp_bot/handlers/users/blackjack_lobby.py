from asyncio import sleep

# from loader import bot

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from games.blackjack.game import game_started
from keyboards.inline.callback_datas import create_lobby_callback, leave_lobby_callback

from keyboards.inline.leave_lobby import leave_lobby_menu
from loader import dp
from states.start_game import StartGame_State
from utils.db_api.blackjack.find_lobby_blackjack import find_lobby_blackjack, delete_lobby_blackjack



@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="blackjack"),
                           state=StartGame_State.game)
async def bot_blackjack_create_lobby(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(chat_id=call.message.chat.id)
    data = await state.get_data()
    game_start = await find_lobby_blackjack(data.get('user_id'), data.get('bet_id'), data.get('chat_id'))
    await call.message.answer(
        f"Вы добавленны в лобби. Поиск игроков...\n",
        parse_mode=types.ParseMode.HTML, reply_markup=leave_lobby_menu)
    if game_start:
        await game_started(game_start)
    await StartGame_State.game.set()


@dp.callback_query_handler(leave_lobby_callback.filter(leave="yes"),
                           state=StartGame_State.game)
async def bot_blackjack_lobby_leave(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    delete_lobby_blackjack(data.get('user_id'))
    await call.message.answer(
        f"Вы отменили поиск игры. Введите /start для доступа к главному меню.\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()

