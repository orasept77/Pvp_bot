
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import deposit_main_callback, deposit_withdrawal_amount_callback, \
    deposit_deposit_amount_callback, deposit_withdrawal_type_callback
from keyboards.inline.deposit_menu import withdrawal_menu, withdrawal_amount_menu
from loader import dp
from states.deposit import Deposit_State


@dp.callback_query_handler(deposit_main_callback.filter(what_to_do="withdrawal"), state=Deposit_State.what_to_do)
async def bot_choice_game(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(what_to_do="make_deposit")
    await call.message.answer(
        f"Выберете удобную для вас сумму для вывода из меню ниже.\n\n"
        f"На данный момент у вас [ни одной] фишек.\n"
        f"Одна фишка эквивалентна одной гривне.",
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_amount_menu)
    await Deposit_State.amount.set()


@dp.callback_query_handler(deposit_withdrawal_amount_callback.filter(amount=["50", "100", "200", "500"]), state=Deposit_State.amount)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(amount=callback_data.get('amount'))
    await call.message.answer(
        f"Вы выбрали вывод на {callback_data.get('amount')} фишек.\n\n"
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"Доступные способы пополнения:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_menu)
    await Deposit_State.purchase_type.set()


@dp.callback_query_handler(deposit_withdrawal_amount_callback.filter(amount="another"), state=Deposit_State.amount)
async def bot_deposit_makedeposit_another(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(amount="amount")

    await call.message.answer(
        f"Введите желаемую сумму для вывода при помощи клавиатуры.",
        parse_mode=types.ParseMode.HTML)
    await Deposit_State.purchase_type.set()


@dp.callback_query_handler(deposit_withdrawal_type_callback.filter(type="card_privatbank"), state=Deposit_State.purchase_type)
async def bot_choice_game(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(purchase_type="card_privatbank")
    await call.message.answer(
        f"Вы выбрали вывод на карту ПриватБанка.\n\n"
        f"Пожалуйста, укажите необходимые данные для перевода.\n\n"
        f"*СПИСОК ДАННЫХ"
        f"Будьте внимательны при предоставлении данных,"
        f"в случае ошибки при заполнении формы - ваши фишки могут быть утерянны."
        f"Все данные являются приватными и не передаются третьим лицам.",
        parse_mode=types.ParseMode.HTML)
    await state.finish()