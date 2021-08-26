
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import deposit_main_callback, deposit_withdrawal_amount_callback, deposit_withdrawal_type_callback
from keyboards.inline.deposit_menu.deposit_menu import withdrawal_menu, withdrawal_amount_menu, \
    withdrawal_type_back_menu, withdrawal_amount_back_menu
from loader import dp
from states.deposit import Deposit_State
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo


@dp.callback_query_handler(deposit_main_callback.filter(what_to_do="withdrawal"))
async def bot_deposit_withdrawal(call:CallbackQuery, state: FSMContext):
    await state.update_data(what_to_do="make_deposit")
    conn = await create_conn("conn_str")
    deposit_repo = DepositRepo(conn=conn)
    user_deposit = await deposit_repo.get_user_deposit(call.from_user.id)
    await call.message.edit_text(
        f"Выберете удобную для вас сумму для вывода из меню ниже.\n\n"
        f"На данный момент у вас [{user_deposit[2]}] фишек.\n"
        f"Одна фишка эквивалентна одной гривне.",
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_amount_menu)
    await conn.close()

@dp.callback_query_handler(deposit_withdrawal_amount_callback.filter(amount=["50", "100", "200", "500"]))
async def bot_deposit_withdrawal_amount(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(amount=callback_data.get('amount'))
    await call.message.edit_text(
        f"Вы выбрали вывод на {callback_data.get('amount')} фишек.\n\n"
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"Доступные способы пополнения:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_menu)


@dp.callback_query_handler(deposit_withdrawal_amount_callback.filter(amount="another"))
async def bot_deposit_makedeposit_another(call:CallbackQuery, state: FSMContext):
    await state.update_data(amount="amount")
    await call.message.edit_text(
        f"Введите желаемую сумму для вывода при помощи клавиатуры.",
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_amount_back_menu)


@dp.callback_query_handler(deposit_withdrawal_type_callback.filter(type="card_privatbank"))
async def bot_deposit_withdrawal_type(call:CallbackQuery, state: FSMContext):
    await state.update_data(purchase_type="card_privatbank")
    await call.message.edit_text(
        f"Вы выбрали вывод на карту ПриватБанка.\n\n"
        f"Пожалуйста, укажите необходимые данные для перевода.\n\n"
        f"*СПИСОК ДАННЫХ"
        f"Будьте внимательны при предоставлении данных,"
        f"в случае ошибки при заполнении формы - ваши фишки могут быть утерянны."
        f"Все данные являются приватными и не передаются третьим лицам.",
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_type_back_menu)
    await state.finish()