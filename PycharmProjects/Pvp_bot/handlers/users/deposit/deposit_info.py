
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import main_menu_callback
from keyboards.inline.deposit_menu.deposit_menu import deposit_menu_main
from loader import dp
from states.deposit import Deposit_State
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo


@dp.callback_query_handler(main_menu_callback.filter(menu_choice="deposit"), state=None)
async def bot_choice_game(call:CallbackQuery):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    deposit_repo = DepositRepo(conn=conn)
    user_deposit = await deposit_repo.get_user_deposit(call.from_user.id)
    await call.message.answer(
        f"Ваш депозит составляет [{user_deposit[2]}] фишек.\n\n"
        f"Вы можете пополнить или вывести свой депозит в любое время.\n\n"
        f"Доступные способы оплаты:\n"
        f"  *ПриватБанк\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu_main)
    await Deposit_State.what_to_do.set()
    await conn.close()