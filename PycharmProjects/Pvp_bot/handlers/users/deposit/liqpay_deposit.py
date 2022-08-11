from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data.messages_text.deposit.liqpay_deposit import create_liqpay_deposit_start_msg, create_liqpay_deposit_stop_msg, \
    create_liqpay_phone_number_is_not_text_msg, create_liqpay_check_user_data_msg, create_liqpay_deposit_make_order_msg
from keyboards.inline.callback_datas import liqpay_deposit_start_callback, liqpay_deposit_stop_callback, \
    liqpay_deposit_data_is_correct_callback
from keyboards.inline.liqpay.liqpay_deposit_start import liqpay_stop_deposit_state, liqpay_deposit_data_is_correct
from keyboards.inline.main_menu import to_menu
from loader import dp
from states.liqpay_states import LiqPayDeposit
from utils.liqpay_api.liqpay import liqpay_create_deposit_payment


@dp.callback_query_handler(liqpay_deposit_start_callback.filter(start_deposit_liqpay_dialog="start"))
async def bot_liqpay_deposit_start_dialog(call: CallbackQuery, state: FSMContext):
    await state.update_data(purchase_type="liqpay")
    text_for_user = await create_liqpay_deposit_start_msg()
    await LiqPayDeposit.typing_phone.set()
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_deposit_state)


@dp.message_handler(state=LiqPayDeposit.typing_phone)
async def bot_liqpay_deposit_check_user_data(message:Message, state: FSMContext):
    if message.text.isnumeric():
        phone_number = int(message.text)
        await state.update_data(phone_number=phone_number)
        text_for_user = await create_liqpay_check_user_data_msg(phone_number)
        await message.answer(
            text=text_for_user,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_deposit_data_is_correct)
    else:
        text = await create_liqpay_phone_number_is_not_text_msg()
        await message.answer(
            text=text,
            parse_mode=types.ParseMode.HTML, reply_markup=liqpay_stop_deposit_state)


@dp.callback_query_handler(liqpay_deposit_data_is_correct_callback.filter(correct="true"), state='*')
async def bot_liqpay_deposit_make_order(call:CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phone_number = data.get('phone_number')
    amount = data.get('amount')
    text_for_user = await create_liqpay_deposit_make_order_msg(phone_number=phone_number, amount=amount)
    payment = await liqpay_create_deposit_payment(user_id=call.from_user.id, amount=int(amount), phone=str(phone_number))
    print(payment)
    await state.finish()
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=to_menu())


@dp.callback_query_handler(liqpay_deposit_stop_callback.filter(stop="true"), state='*')
async def bot_liqpay_deposit_stop(call:CallbackQuery, state: FSMContext):
    text_for_user = await create_liqpay_deposit_stop_msg()
    await state.finish()
    await call.message.edit_text(
        text=text_for_user,
        parse_mode=types.ParseMode.HTML, reply_markup=to_menu())