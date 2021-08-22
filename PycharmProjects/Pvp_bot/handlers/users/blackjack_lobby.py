from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.blackjack_menu import blackjack_menu
from keyboards.inline.callback_datas import create_lobby_callback, lobby_ready_callback
from keyboards.inline.cancel_menu import cancel_menu
from keyboards.inline.game_ready import game_ready_menu
from loader import dp
from states.start_game import StartGame_State
from utils.db_api.blackjack.find_lobby_blackjack import find_lobby_blackjack
from utils.db_api.find_room_is_full import change_room_state_on_playing, \
    change_room_state_on_aborted, check_is_room_is_full_and_not_aborted


@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="blackjack"),
                           state=StartGame_State.game)
async def bot_blackjack_create_lobby(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    print(data.get('user_id'))
    print(data.get('bet_id'))
    find_lobby_blackjack(data.get('user_id'), data.get('bet_id'))



@dp.callback_query_handler(lobby_ready_callback.filter(status="abort"),
                           state=StartGame_State.game)
async def bot_blackjack_lobby_aborted(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    change_room_state_on_aborted(data.get('room_number'))
    await call.message.answer(
        f"Вы отменили игру. Введите /start для доступа к главному меню.\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()

