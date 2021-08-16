
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import aiogram.utils.markdown as fmt

from keyboards.default.deposit_menu import withdrawal_menu
from loader import dp


@dp.message_handler(Text(equals="🃏 Вывести 🃏", ignore_case=True), state="*")
async def bot_deposit_withdrawal_main(message: types.Message):
    await message.answer(
        f"Для вывода депозита выберите предпочитаемый способ получения из меню ниже.\n\n"
        f"На данный момент у вас [ни одной] фишек.\n"
        f"Одна фишка эквивалентна одной гривне.\n\n"
        f"Доступные способы вывода:\n"
        f"  *Карта ПриватБанка",
        parse_mode=types.ParseMode.HTML, reply_markup=withdrawal_menu)


@dp.message_handler(Text(equals="💳 Вывести на карту (Приватбанк) 💳", ignore_case=True), state="*")
async def bot_deposit_withdrawal_privatbank(message: types.Message):
    await message.answer(
        f"Вы выбрали вывод на карту ПриватБанка.\n\n"
        f"Пожалуйста, укажите необходимые данные для перевода.\n\n"
        f"*СПИСОК ДАННЫХ"
        f"Будьте внимательны при предоставлении данных,"
        f"в случае ошибки при заполнении формы - ваши фишки могут быть утерянны."
        f"Все данные являются приватными и не передаются третьим лицам.",
        parse_mode=types.ParseMode.HTML)
