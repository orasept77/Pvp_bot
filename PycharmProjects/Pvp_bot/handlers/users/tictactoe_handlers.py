from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import create_lobby_callback, choice_game_type_callback
from keyboards.inline.choose_game_menu.game_connect_to_the_friend_menu import connect_to_the_friend_menu
from loader import dp
from states.start_game import StartGame_State
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.rates.rates_repo import RatesRepo


@dp.callback_query_handler(create_lobby_callback.filter(game_type=["random_player", "play_with_friend"]),
                           state=StartGame_State.game)

async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    rates_repo = RatesRepo(conn=conn)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.answer(
        f"Вы выбрали игру *НАЗВАНИЕ ИГРЫ*\n"
        f"Ваш депозит составляет [минус тыща] фишек.\n\n"
        f"Выберите наиболее интересующую вас ставку их меню ниже.\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=await rates_repo.get_rates_data())
    await StartGame_State.type.set()
    conn.close()



@dp.callback_query_handler(choice_game_type_callback.filter(game_type=["connect_to_the_friend"]),
                           state=StartGame_State.type)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.answer(
        f"Вы выбрали игру *НАЗВАНИЕ ИГРЫ*\n"
        f"Ваш депозит составляет [минус тыща] фишек.\n"
        f"Для подключения у вас должно быть достаточно фишек на счету.\n\n"
        f"Введите ИД комнаты для подключения к другу.\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=connect_to_the_friend_menu)
