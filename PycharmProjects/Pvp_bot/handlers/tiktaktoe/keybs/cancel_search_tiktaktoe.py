from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
cancel_search_tiktaktoe_cb = "cancel_search_tiktaktoe_cb"

def cancel_search_tiktaktoe_keyb():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Отмена", callback_data=cancel_search_tiktaktoe_cb))
    return markup