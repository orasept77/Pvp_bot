from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.account.account_change_nickname import account_change_nickname_keyb
from keyboards.inline.account.account_main_menu import account_menu_keyb
from keyboards.inline.callback_datas import account_main_callback, main_menu_callback, account_change_nickname_cb, \
    account_change_nickname_callback

from loader import dp
from states.account_change_nickname import AccountChangeNichname
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.user.user_repo import UserRepo


@dp.callback_query_handler(account_main_callback.filter(enter="true"), state="*")
async def bot_account_main(call:CallbackQuery):
    conn = await create_conn()
    user_repo = UserRepo(conn=conn)
    deposit_repo = DepositRepo(conn=conn)
    user = await user_repo.get_user(call.from_user.id)
    if user:
        back_button = InlineKeyboardButton("🔽   Назад   🔽", callback_data=main_menu_callback.new(menu_choice="main_menu"))
        user_balance = await deposit_repo.get_user_deposit(call.from_user.id)
        await call.message.edit_text(
            f"Добро пожаловать в ваш личный кабинет.\n\n"
            f"Данные вашего профиля:\n"
            f"Ваш ID: {user['id']}\n"
            f"Имя пользователя: @{user['username']}\n"
            f"Ник: {user['first_name']}\n"
            f"Кастомный ник: {user['custom_nick']}\n\n"
            f"Количество фишек: {user_balance[2]}\n\n"
            f"В этом меню вы можете посмотреть вашу статистику, а так-же топ игроков по набранным очкам.\n"
            f"Для доступа к вашему депозиту выберете 'Депозит'\n"
            f"Если данные в играх о вашем аккаунте отображатся не верно, вы можете обновить их нажав кнопку 'Обновить данные'\n\n"
            f"Выберете интересующую вас опцию из меню ниже.",
            parse_mode=types.ParseMode.HTML, reply_markup=account_menu_keyb([back_button]))
        await conn.close()
    else:
        await call.message.answer("user not found")


@dp.callback_query_handler(account_change_nickname_cb.filter(change="yes"), state="*")
async def bot_account_change_nickname_question(call:CallbackQuery):
    conn = await create_conn()
    user_repo = UserRepo(conn=conn)
    user = await user_repo.get_user(call.from_user.id)
    if user:
        await call.message.edit_text(
            f"Ваш текущий кастомный ник: {user['custom_nick']}.\n\n"
            f"Вы уверены что хотите его сменить?:\n",
            parse_mode=types.ParseMode.HTML, reply_markup=account_change_nickname_keyb())
        await conn.close()
    else:
        await call.message.answer("user not found")


@dp.callback_query_handler(account_change_nickname_callback.filter(button="yes"), state="*")
async def bot_account_change_nickname(call:CallbackQuery, state: FSMContext):
    conn = await create_conn()
    user_repo = UserRepo(conn=conn)
    user = await user_repo.get_user(call.from_user.id)
    await state.update_data(last_message_id=call.message.message_id)
    if user:
        await AccountChangeNichname.typing.set()
        await call.message.edit_text(
            f"Введите ваш новый ник.\n",
            parse_mode=types.ParseMode.HTML)
        await conn.close()
    else:
        await call.message.answer("user not found")


@dp.message_handler(state=AccountChangeNichname.typing)
async def bot_account_change_nickname_done(message:Message, state: FSMContext):
    conn = await create_conn()
    user_repo = UserRepo(conn=conn)
    user = await user_repo.get_user(message.from_user.id)
    if user:
        markup = InlineKeyboardMarkup(resize_keyboard=True)
        markup.add(InlineKeyboardButton("🔽   Назад   🔽", callback_data=account_main_callback.new(enter="true")))
        if len(message.text) < 30:
            await user_repo.set_custom_nick(message.from_user.id, message.text)
            user = await user_repo.get_user(message.from_user.id)
            await message.answer(
                f"Вы успешно сменили ник, {user['custom_nick']}.\n",
                parse_mode=types.ParseMode.HTML, reply_markup=markup)
            await state.finish()
            await conn.close()
        else:
            await message.answer(
                f"Слишком длинный никнейм. Максимальная длинна: 30 символов.\n",
                parse_mode=types.ParseMode.HTML, reply_markup=account_menu_keyb([back_button]))
    else:
        await message.answer("user not found")
        await state.finish()