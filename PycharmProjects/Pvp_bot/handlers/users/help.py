from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from keyboards.inline.cancel_menu import cancel_menu
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(
        f"У вас возникли вопросы или какие либо технические проблемы?.\n\n"
        f"Свяжитесь с нами и подробно опишите проблему:\n"
        f"*контакты службы поддержки*",
        parse_mode=types.ParseMode.HTML, reply_markup=cancel_menu)