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
from utils.db_api.find_room_for_blackjack import find_empty_room_for_blackjack
from utils.db_api.find_room_is_full import check_is_room_is_full, change_room_state_on_playing, \
    change_room_state_on_aborted


@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="blackjack"),
                           state=StartGame_State.game)
async def bot_blackjack_create_lobby(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    room_number = find_empty_room_for_blackjack(call.from_user)
    await state.update_data(room_number=room_number)
    await call.message.answer(
        f"Идёт поиск лобби для игры.\n",
        parse_mode=types.ParseMode.HTML, reply_markup=cancel_menu)
    while check_is_room_is_full(room_number) is not True:
        await sleep(10)
        await call.message.answer(
            f"Ожидаем соперника.\n",
            parse_mode=types.ParseMode.HTML)
    change_room_state_on_playing(room_number)
    await call.message.answer(
        f"Соперник найден. Нажмите кнопку 'Готов для начала игры'.\n",
        parse_mode=types.ParseMode.HTML, reply_markup=game_ready_menu)
    await StartGame_State.game.set()


@dp.callback_query_handler(lobby_ready_callback.filter(status="start"),
                           state=StartGame_State.game)
async def bot_blackjack_give_first_cards(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer(
        f"Ожидаем когда соперник приймет игру.\n",
        parse_mode=types.ParseMode.HTML)
    await call.message.answer(
        f"Игра начинается!\n",
        parse_mode=types.ParseMode.HTML)
    await call.message.answer(
        f"Раздаём карты. Каждый игрок получил по 2 карты.\n"
        f"Выбирите, хотите ли вы взять ещё одну карту или остановиться.",
        parse_mode=types.ParseMode.HTML, reply_markup=blackjack_menu)
    await StartGame_State.game.set()


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

