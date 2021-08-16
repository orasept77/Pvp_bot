from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import aiogram.utils.markdown as fmt

from keyboards.default.deposit_menu import deposit_menu, deposit_amount_menu
from loader import dp


@dp.message_handler(Text(equals="❌ Пополнить ⭕", ignore_case=True), state="*")
async def bot_deposit_makedeposit_main(message: types.Message):
    await message.answer(
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"На данный момент у вас [ни одной] фишек.\n"
        f"Одна фишка эквивалентна одной гривне.\n\n",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_amount_menu)


@dp.message_handler(Text(equals="50 фишек", ignore_case=True), state="*")
async def bot_deposit_makedeposit_50(message: types.Message):
    await message.answer(
        f"Вы выбрали пополнение на 50 фишек.\n\n"
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"Доступные способы пополнения:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu)


@dp.message_handler(Text(equals="100 фишек", ignore_case=True), state="*")
async def bot_deposit_makedeposit_100(message: types.Message):
    await message.answer(
        f"Вы выбрали пополнение на 100 фишек.\n\n"
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"Доступные способы пополнения:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu)


@dp.message_handler(Text(equals="200 фишек", ignore_case=True), state="*")
async def bot_deposit_makedeposit_200(message: types.Message):
    await message.answer(
        f"Вы выбрали пополнение на 200 фишек.\n\n"
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"Доступные способы пополнения:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu)


@dp.message_handler(Text(equals="⭐ 500 фишек ⭐", ignore_case=True), state="*")
async def bot_deposit_makedeposit_500(message: types.Message):
    await message.answer(
        f"Вы выбрали пополнение на 500 фишек.\n\n"
        f"Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"Доступные способы пополнения:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu)


@dp.message_handler(Text(equals="Другая сумма", ignore_case=True), state="*")
async def bot_deposit_makedeposit_another(message: types.Message):
    await message.answer(
        f"Введите желаемую сумму для пополнения при помощи клавиатуры.",
        parse_mode=types.ParseMode.HTML)


# Добавить логику где пользователь выбирает себе сумму


@dp.message_handler(Text(equals="💳 Пополнить картой (Приватбанк) 💳", ignore_case=True), state="*")
async def bot_deposit_makedeposit_privatbank(message: types.Message):
    await message.answer(
        f"Вы выбрали пополнение картой ПриватБанка.\n\n"
        f"Пожалуйста, укажите необходимые данные для перевода.\n\n"
        f"*СПИСОК ДАННЫХ"
        f"Будьте внимательны при предоставлении данных,"
        f"в случае ошибки при заполнении формы - ваши фишки могут быть утерянны."
        f"Все данные являются приватными и не передаются третьим лицам.",
        parse_mode=types.ParseMode.HTML)
