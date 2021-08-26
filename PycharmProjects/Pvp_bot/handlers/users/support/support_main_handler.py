from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import support_callback
from keyboards.inline.cancel_menu import cancel_menu
from loader import dp


@dp.callback_query_handler(support_callback.filter(to_do="get_info"), state="*")
async def bot_account_main(call:CallbackQuery):
    await call.message.edit_text(
        f"У вас возникли вопросы или какие либо технические проблемы?.\n\n"
        f"Свяжитесь с нами и подробно опишите проблему:\n"
        f"*контакты службы поддержки*",
        parse_mode=types.ParseMode.HTML, reply_markup=cancel_menu)