from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import CallbackQuery

from data.messages_text.deposit.deposit_deposits import create_deposit_choose_amount_msg, \
    create_deposit_choose_type_msg, create_deposit_write_amount_msg, create_deposit_liqpay_start_msg
from keyboards.inline.callback_datas import deposit_main_callback, \
    deposit_deposit_type_callback, deposit_deposit_amount_callback, cancel_callback
from keyboards.inline.deposit_menu.deposit_menu import deposit_amount_menu, deposit_menu, deposit_amount_back_menu, \
    deposit_type_back_menu
from keyboards.inline.liqpay.liqpay_deposit_start import liqpay_deposit_start_menu
from loader import dp
from states.deposit import Deposit_State
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo


@dp.callback_query_handler(deposit_main_callback.filter(what_to_do="deposit"))
async def bot_choice_game(call:CallbackQuery, state: FSMContext):
    conn = await create_conn()
    deposit_repo = DepositRepo(conn=conn)
    user_deposit = await deposit_repo.get_user_deposit(call.from_user.id)
    text_for_user = await create_deposit_choose_amount_msg(user_deposit)
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_amount_menu)
    await conn.close()


@dp.callback_query_handler(deposit_deposit_amount_callback.filter(amount=["50", "100", "200", "500"]))
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(amount=callback_data.get('amount'))
    text_for_user = await create_deposit_choose_type_msg(callback_data.get('amount'))
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu)


# @dp.callback_query_handler(deposit_deposit_amount_callback.filter(amount="another"))
# async def bot_deposit_makedeposit_another(call:CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=60)
#     await state.update_data(amount="amount")
#     text_for_user = await create_deposit_write_amount_msg()
#     await call.message.edit_text(
#         text=text_for_user,
#         parse_mode=types.ParseMode.HTML, reply_markup=deposit_amount_back_menu)


@dp.callback_query_handler(deposit_deposit_type_callback.filter(type="liqpay_phone_number"))
async def bot_pre_start_liqpay_dialog(call: CallbackQuery, state: FSMContext):
    await state.update_data(purchase_type="liqpay_phone_number")
    data = await state.get_data()
    text_for_user = await create_deposit_liqpay_start_msg(data.get('amount'))
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=liqpay_deposit_start_menu)