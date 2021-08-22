from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from keyboards.inline.callback_datas import cancel_callback

tiktaktoe_callback = CallbackData("tiktaktoe_callback", "rates_id")


def start_tiktaktoe(rates_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Старт", callback_data=tiktaktoe_callback.new(rates_id=rates_id)))
    markup.add(InlineKeyboardButton(text="Отмена", callback_data=cancel_callback.new(status="cancel")))
    return markup