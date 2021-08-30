from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton

from keyboards.inline.callback_datas import choice_game_callback, main_menu_callback
from keyboards.inline.choose_game_menu.choose_game_type_menu import choose_game_type_menu_keyb
from loader import dp
from states.start_game import StartGame_State
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo


@dp.callback_query_handler(choice_game_callback.filter(game=["Крестики-Нолики", "Блек-Джек", "Камень-Ножницы-Бумага"]))
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(game_name=callback_data.get('game'))
    await state.update_data(user_id=call.from_user.id)
    conn = await create_conn("conn_str")
    deposit_repo = DepositRepo(conn=conn)
    user_deposit = await deposit_repo.get_user_deposit(call.from_user.id)
    data = await state.get_data()
    back_button = InlineKeyboardButton("🔽   Назад   🔽", callback_data=main_menu_callback.new(menu_choice="choice_game"))
    await call.message.edit_text(
        f"Вы выбрали игру {callback_data.get('game')}\n"
        f"Ваш депозит составляет [{user_deposit[2]}] фишек.\n\n"
        f"Выберите интересующий вас тип игры:\n"
        f"  *Случайный противник - вам будет подобран случайный оппонент.\n"
        f"  *Играть с другом - вы получите уникальный ИД который вы должны будете передать вашему другу.\n\n"
        f"Для управления нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=choose_game_type_menu_keyb([back_button]))
    await conn.close()

