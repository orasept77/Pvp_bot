from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.messages_text.deposit.deposit_withdrawals import create_withdrawals_choose_amount_msg, \
    create_withdrawals_choose_type_msg, create_withdrawals_write_amount_msg, create_withdrawals_liqpay_start_msg
from keyboards.inline.callback_datas import deposit_main_callback, deposit_withdrawal_amount_callback, \
    deposit_withdrawal_type_callback
from keyboards.inline.deposit_menu.deposit_menu import withdrawal_menu, withdrawal_amount_menu, \
    withdrawal_type_back_menu, withdrawal_amount_back_menu
from keyboards.inline.liqpay.liqpay_withdrawal_start import liqpay_withdrawal_start_dialog_menu
from loader import dp
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo


@dp.callback_query_handler(deposit_main_callback.filter(what_to_do="withdrawal"))
async def bot_deposit_withdrawal(call: CallbackQuery, state: FSMContext):
    await state.update_data(what_to_do="withdrawal")
    conn = await create_conn()
    deposit_repo = DepositRepo(conn=conn)
    user_deposit = await deposit_repo.get_user_deposit(call.from_user.id)
    text_for_user = await create_withdrawals_choose_amount_msg(user_deposit)
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_amount_menu)
    await conn.close()


@dp.callback_query_handler(deposit_withdrawal_amount_callback.filter(amount=["50", "100", "200", "500"]))
async def bot_deposit_withdrawal_amount(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(amount=callback_data.get('amount'))
    text_for_user = await create_withdrawals_choose_type_msg(callback_data.get('amount'))
    conn = await create_conn()
    depo = DepositRepo(conn=conn)
    balance = await depo.get_user_balance(call.from_user.id)
    if balance['balance'] < int(callback_data.get('amount')):
        await call.answer("Недостаточный баланс для этого действия.", show_alert=True)
    else:
        await call.message.edit_text(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_menu)


# @dp.callback_query_handler(deposit_withdrawal_amount_callback.filter(amount="another"))
# async def bot_deposit_makedeposit_another(call: CallbackQuery, state: FSMContext):
#     await state.update_data(amount="amount")
#     text_for_user = await create_withdrawals_write_amount_msg()
#     await call.message.edit_text(
#         text=text_for_user,
#         parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_amount_back_menu)


@dp.callback_query_handler(deposit_withdrawal_type_callback.filter(type=["liqpay_phone_number", "liqpay_card_number", "liqpay_email"]))
async def bot_liqpay_withdrawals_pre_starting_dialog(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(purchase_type=callback_data.get('type'))
    data = await state.get_data()
    payment_type = data.get('purchase_type')
    if payment_type == "liqpay_phone_number":
        payment_type = "По номеру телефона"
    elif payment_type == "liqpay_card_number":
        payment_type = "По номеру карты"
    elif payment_type == "liqpay_email":
        payment_type = "По email"
    text_for_user = await create_withdrawals_liqpay_start_msg(data.get('amount'), payment_type)
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=liqpay_withdrawal_start_dialog_menu)

