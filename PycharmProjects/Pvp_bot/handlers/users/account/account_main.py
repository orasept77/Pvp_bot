from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.account.account_main_menu import account_menu
from keyboards.inline.callback_datas import account_main_callback

from loader import dp
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.user.user_repo import UserRepo


@dp.callback_query_handler(account_main_callback.filter(enter="true"))
async def bot_account_main(call:CallbackQuery):
    conn = await create_conn("conn_str")
    user_repo = UserRepo(conn=conn)
    deposit_repo = DepositRepo(conn=conn)
    user = await user_repo.get_user(call.from_user.id)
    user_balance = await deposit_repo.get_user_deposit(call.from_user.id)
    await call.message.answer(
        f"Добро пожаловать в ваш личный кабинет.\n\n"
        f"Данные вашего профиля:\n"
        f"Ваш ID: {user[0][0]}\n"
        f"Имя пользователя: @{user[0][3]}\n"
        f"Имя: {user[0][1]}\n"
        f"Фамилия: {user[0][2]}\n\n"
        f"Количество фишек: {user_balance[2]}\n"
        f"В этом меню вы можете посмотреть вашу статистику, а так-же топ игроков по набранным очкам.\n"
        f"Для доступа к вашему депозиту выберете 'Депозит'\n"
        f"Если данные в играх о вашем аккаунте отображатся не верно, вы можете обновить их нажав кнопку 'Обновить данные'\n\n"
        f"Выберете интересующую вас опцию из меню ниже.",
        parse_mode=types.ParseMode.HTML, reply_markup=account_menu)
    await conn.close()