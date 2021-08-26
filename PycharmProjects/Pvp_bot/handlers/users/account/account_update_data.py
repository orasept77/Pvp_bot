from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import aiogram.utils.markdown as fmt
from aiogram.types import CallbackQuery

from keyboards.inline.account.account_update_info_menu import account_update_info_menu
from keyboards.inline.callback_datas import account_update_data_callback
from keyboards.inline.main_menu import main_menu
from loader import dp
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.user.user_repo import UserRepo


@dp.callback_query_handler(account_update_data_callback.filter(enter="true"))
async def bot_account_update_data(call:CallbackQuery):
    conn = await create_conn("conn_str")
    user_repo = UserRepo(conn=conn)
    await user_repo.update_user(call.from_user.id, call.from_user.first_name, call.from_user.last_name, call.from_user.username)
    await call.message.edit_text(
        f"Уважаемый {call.from_user.first_name} [@{call.from_user.username}],\n\n"
        f"Ваши данные профиля были обновленны в меру открытости вашего профиля.\n\n"
        f"Новые обновлённые данные профиля:\n"
        f"Ваш ID: {call.from_user.id}\n"
        f"Ваше имя пользователя: @{call.from_user.username}\n"
        f"Ваш ник: {call.from_user.first_name}\n",
        parse_mode=types.ParseMode.HTML, reply_markup=account_update_info_menu)
    await conn.close()