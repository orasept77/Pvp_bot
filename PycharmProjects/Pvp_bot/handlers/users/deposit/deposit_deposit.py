from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import deposit_main_callback, \
    deposit_deposit_type_callback, deposit_deposit_amount_callback, cancel_callback
from keyboards.inline.deposit_menu.deposit_menu import deposit_amount_menu, deposit_menu, deposit_amount_back_menu, \
    deposit_type_back_menu
from loader import dp
from states.deposit import Deposit_State
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo


@dp.callback_query_handler(deposit_main_callback.filter(what_to_do="deposit"))
async def bot_choice_game(call:CallbackQuery, state: FSMContext):
    conn = await create_conn()
    deposit_repo = DepositRepo(conn=conn)
    user_deposit = await deposit_repo.get_user_deposit(call.from_user.id)
    await call.message.edit_text(
        f"Пожалуйста, укажите сумму для пополнения из меню нижу.\n\n"
        f"На данный момент у вас [{user_deposit[2]}] фишек.\n"
        f"Одна фишка эквивалентна одной гривне.",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_amount_menu)
    await conn.close()


@dp.callback_query_handler(deposit_deposit_amount_callback.filter(amount=["50", "100", "200", "500"]))
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(amount=callback_data.get('amount'))
    await call.message.edit_text(
        f"Вы выбрали пополнение на {callback_data.get('amount')} фишек.\n\n"
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"Доступные способы пополнения:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu)


@dp.callback_query_handler(deposit_deposit_amount_callback.filter(amount="another"))
async def bot_deposit_makedeposit_another(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(amount="amount")
    await call.message.edit_text(
        f"Введите желаемую сумму для пополнения при помощи клавиатуры.",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_amount_back_menu)


@dp.callback_query_handler(deposit_deposit_type_callback.filter(type="card_privatbank"))
async def bot_choice_game(call:CallbackQuery, state: FSMContext):
    await state.update_data(purchase_type="card_privatbank")
    await call.message.edit_text(
        f"Вы выбрали пополнение картой ПриватБанка.\n\n"
        f"Пожалуйста, укажите необходимые данные для перевода.\n\n"
        f"*СПИСОК ДАННЫХ*\n\n"
        f"Будьте внимательны при предоставлении данных,"
        f"в случае ошибки при заполнении формы - ваши фишки могут быть утерянны."
        f"Все данные являются приватными и не передаются третьим лицам.",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_type_back_menu)