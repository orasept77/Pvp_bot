from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
tiktaktoe_callback = CallbackData("tiktaktoe_callback", "rates_id")

def start_tiktaktoe(rates_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Старт", callback_data=tiktaktoe_callback.new(
                            rates_id=rates_id
            )))
    markup.add(InlineKeyboardButton(text="Отмена", callback_data=tiktaktoe_callback.new(
                            rates_id=rates_id
            )))
    return markup