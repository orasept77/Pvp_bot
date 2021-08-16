
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import aiogram.utils.markdown as fmt

from keyboards.default.deposit_menu import deposit_menu_main
from loader import dp


@dp.message_handler(Text(equals="💰 Депозит 💰", ignore_case=True), state="*")
async def bot_deposit(message: types.Message):
    await message.answer(
        f"Ваш депозит составляет [минус тыща] фишек.\n\n"
        f"Вы можете пополнить или вывести свой депозит в любое время.\n\n"
        f"Доступные способы оплаты:\n"
        f"  *ПриватБанк\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=deposit_menu_main)