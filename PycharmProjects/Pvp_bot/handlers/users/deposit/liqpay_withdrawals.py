from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data.messages_text.deposit.liqpay_deposit import create_liqpay_deposit_stop_msg, \
    create_liqpay_phone_number_is_not_text_msg, create_liqpay_check_user_data_msg, create_liqpay_deposit_make_order_msg
from data.messages_text.deposit.liqpay_withdrawals import create_liqpay_withdrawals_phone_start_msg, \
    create_liqpay_withdrawals_card_start_msg, create_liqpay_withdrawals_email_start_msg, \
    create_liqpay_withdrawals_phone_number_is_not_text_msg, create_liqpay_withdrawals_card_number_is_not_text_msg, \
    create_liqpay_withdrawals_check_user_data_msg_phone_1, create_liqpay_withdrawals_check_user_data_msg_card_1, \
    create_liqpay_withdrawals_check_user_data_msg_email_1, create_liqpay_withdrawals_check_user_data_msg_phone_2, \
    create_liqpay_withdrawals_check_user_data_msg_card_2, create_liqpay_withdrawals_check_user_data_msg_email_2, \
    create_liqpay_withdrawals_check_user_data_msg_phone_done, create_liqpay_withdrawals_check_user_data_msg_card_done, \
    create_liqpay_withdrawals_check_user_data_msg_email_done, create_liqpay_withdrawals_make_order_phone_msg, \
    create_liqpay_withdrawals_make_order_card_msg, create_liqpay_withdrawals_make_order_email_msg
from keyboards.inline.callback_datas import liqpay_withdrawal_stop_callback, \
    liqpay_withdrawal_data_is_correct_callback, liqpay_withdrawal_starting_dialogue_callback
from keyboards.inline.liqpay.liqpay_withdrawal_start import liqpay_stop_withdrawal_state, \
    liqpay_withdrawal_data_is_correct
from keyboards.inline.main_menu import to_menu
from loader import dp
from states.liqpay_states import LiqPayWithdrawal
from utils.liqpay_api.liqpay import liqpay_create_withdrawal_payment_by_email, liqpay_create_withdrawal_payment_by_card, \
    liqpay_create_withdrawal_payment_by_phone


@dp.callback_query_handler(liqpay_withdrawal_starting_dialogue_callback.filter(start_withdrawal_dialogue="start"))
async def bot_liqpay_withdrawals_starting_dialog(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment_type = data.get("purchase_type")
    if payment_type == "liqpay_phone_number":
        text_for_user = await create_liqpay_withdrawals_phone_start_msg()
        await LiqPayWithdrawal.typing_phone.set()
        await state.update_data(last_message_id=call.message.message_id)
        await call.message.edit_text(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)
    if payment_type == "liqpay_card_number":
        text_for_user = await create_liqpay_withdrawals_card_start_msg()
        await LiqPayWithdrawal.typing_card.set()
        await state.update_data(last_message_id=call.message.message_id)
        await call.message.edit_text(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)
    if payment_type == "liqpay_email":
        text_for_user = await create_liqpay_withdrawals_email_start_msg()
        await LiqPayWithdrawal.typing_email.set()
        await state.update_data(last_message_id=call.message.message_id)
        await call.message.edit_text(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)


@dp.message_handler(state=LiqPayWithdrawal.typing_phone)
async def bot_liqpay_withdrawals_phone_next_data(message: Message, state: FSMContext):
    if message.text.isnumeric():
        phone_number = int(message.text)
        await state.update_data(phone_number=phone_number)
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_phone_1(phone_number)
        await LiqPayWithdrawal.typing_first_name.set()
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)
    else:
        text = await create_liqpay_withdrawals_phone_number_is_not_text_msg()
        await message.answer(
            text=text,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)


@dp.message_handler(state=LiqPayWithdrawal.typing_card)
async def bot_liqpay_withdrawals_card_next_data(message: Message, state: FSMContext):
    if message.text.isnumeric():
        card_number = int(message.text)
        await state.update_data(card_number=card_number)
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_card_1(card_number)
        await LiqPayWithdrawal.typing_first_name.set()
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)
    else:
        text = await create_liqpay_withdrawals_card_number_is_not_text_msg()
        await message.answer(
            text=text,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)


@dp.message_handler(state=LiqPayWithdrawal.typing_email)
async def bot_liqpay_withdrawals_email_next_data(message: Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    text_for_user = await create_liqpay_withdrawals_check_user_data_msg_email_1(email)
    await LiqPayWithdrawal.typing_first_name.set()
    await message.answer(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)



@dp.message_handler(state=LiqPayWithdrawal.typing_first_name)
async def bot_liqpay_withdrawals_next_data(message: Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    data = await state.get_data()
    payment_type = data.get("purchase_type")
    if payment_type == "liqpay_phone_number":
        phone_number = data.get("phone_number")
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_phone_2(phone_nubmer=phone_number, user_name=first_name)
        await LiqPayWithdrawal.typing_last_name.set()
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)
    if payment_type == "liqpay_card_number":
        card_number = data.get("card_number")
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_card_2(card_nubmer=card_number, user_name=first_name)
        await LiqPayWithdrawal.typing_last_name.set()
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)
    if payment_type == "liqpay_email":
        email = data.get("email")
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_email_2(email=email, user_name=first_name)
        await LiqPayWithdrawal.typing_last_name.set()
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_withdrawal_state)


@dp.message_handler(state=LiqPayWithdrawal.typing_last_name)
async def bot_liqpay_withdrawals_correct_data(message: Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    data = await state.get_data()
    payment_type = data.get("purchase_type")
    if payment_type == "liqpay_phone_number":
        phone_number = data.get("phone_number")
        first_name = data.get("first_name")
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_phone_done(phone_nubmer=phone_number,
                                                                                    user_name=first_name,
                                                                                       user_lastname=last_name)
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_withdrawal_data_is_correct)
    if payment_type == "liqpay_card_number":
        card_number = data.get("card_number")
        first_name = data.get("first_name")
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_card_done(card_nubmer=card_number,
                                                                                   user_name=first_name, user_lastname=last_name)
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_withdrawal_data_is_correct)
    if payment_type == "liqpay_email":
        email = data.get("email")
        first_name = data.get("first_name")
        text_for_user = await create_liqpay_withdrawals_check_user_data_msg_email_done(email=email, user_name=first_name, user_lastname=last_name)
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_withdrawal_data_is_correct)






@dp.callback_query_handler(liqpay_withdrawal_data_is_correct_callback.filter(correct="true"), state='*')
async def bot_liqpay_withdrawals_make_order(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    amount = data.get("amount")
    payment_type = data.get("purchase_type")
    if payment_type == "liqpay_phone_number":
        phone_number = data.get("phone_number")
        text_for_user = await create_liqpay_withdrawals_make_order_phone_msg(phone_number=phone_number, amount=amount)
        await liqpay_create_withdrawal_payment_by_phone(user_id=call.from_user.id, amount=amount, first_name=first_name, last_name=last_name, user_phone=phone_number)
        await call.message.edit_text(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
    if payment_type == "liqpay_card_number":
        card_number = data.get("card_number")
        text_for_user = await create_liqpay_withdrawals_make_order_card_msg(card_number=card_number, amount=amount)
        await liqpay_create_withdrawal_payment_by_card(user_id=call.from_user.id, amount=amount, first_name=first_name, last_name=last_name, user_card_number=card_number)
        await call.message.edit_text(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
    if payment_type == "liqpay_email":
        email = data.get("email")
        text_for_user = await create_liqpay_withdrawals_make_order_email_msg(email=email, amount=amount)
        await liqpay_create_withdrawal_payment_by_email(user_id=call.from_user.id, amount=amount, first_name=first_name, last_name=last_name, user_email=email)
        await call.message.edit_text(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=to_menu())



@dp.callback_query_handler(liqpay_withdrawal_stop_callback.filter(stop="true"), state='*')
async def bot_liqpay_withdrawals_stop(call: CallbackQuery, state: FSMContext):
    text_for_user = await create_liqpay_deposit_stop_msg()
    await state.finish()
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
