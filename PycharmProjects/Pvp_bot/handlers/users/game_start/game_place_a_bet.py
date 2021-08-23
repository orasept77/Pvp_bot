from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import choice_game_type_callback, make_a_bet_callback, main_menu_callback, \
    cancel_callback
from keyboards.inline.choose_game_menu.game_connect_to_the_friend_menu import connect_to_the_friend_menu
from loader import dp
from states.start_game import StartGame_State
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.rates.rates_repo import RatesRepo

@dp.callback_query_handler(choice_game_type_callback.filter(game_type=["random_player", "play_with_friend"]),
                           state=StartGame_State.type)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    conn = await create_conn("conn_str")
    deposit_repo = DepositRepo(conn=conn)
    rates_repo = RatesRepo(conn=conn)
    user_balance = await deposit_repo.get_user_deposit(call.from_user.id)
    await state.update_data(type=callback_data.get('game_type'))
    data = await state.get_data()
    await call.message.answer(
        f"Вы выбрали игру {data.get('game_name')}\n"
        f"Ваш депозит составляет [{user_balance[2]}] фишек.\n\n"
        f"Выберите наиболее интересующую вас ставку из меню ниже.\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=await rates_repo.get_rates_data())
    await StartGame_State.bet.set()
    await conn.close()


@dp.callback_query_handler(choice_game_type_callback.filter(game_type=["connect_to_the_friend"]),
                           state=StartGame_State.type)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    conn = await create_conn("conn_str")
    deposit_repo = DepositRepo(conn=conn)
    user_balance = await deposit_repo.get_user_deposit(call.from_user.id)
    await state.update_data(type=callback_data.get('game_type'))
    data = await state.get_data()
    await call.message.answer(
        f"Вы выбрали игру {data.get('game_name')}\n"
        f"Ваш депозит составляет [{user_balance[2]}] фишек.\n"
        f"Для подключения у вас должно быть достаточно фишек на счету.\n\n"
        f"Введите ИД комнаты для подключения к другу.\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=connect_to_the_friend_menu)
