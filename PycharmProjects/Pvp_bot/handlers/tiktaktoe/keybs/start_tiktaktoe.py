from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from keyboards.inline.callback_datas import cancel_callback
from keyboards.inline.callback_datas import main_menu_callback

tiktaktoe_callback = CallbackData("tiktaktoe_callback", "rates_id")

tiktaktoe_revansh_cb = CallbackData("tiktaktoe_revansh_cb", "private_lobby_id")

cancel_tiktaktoe_revansh_cb = CallbackData("cancel_tiktaktoe_revansh_cb", "private_lobby_id")

def start_tiktaktoe(rates_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Старт", callback_data=tiktaktoe_callback.new(rates_id=rates_id)))
    markup.add(InlineKeyboardButton(text="Отмена", callback_data=cancel_callback.new(status="cancel")))
    return markup


def tiktaktoe_revansh_keyb(private_lobby_id: int):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Реванш", callback_data=tiktaktoe_revansh_cb.new(
                            private_lobby_id = private_lobby_id

            )))
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")

            ))
    return markup

def cancel_tiktaktoe_revansh_keyb(private_lobby_id: int):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Отменить реванш", callback_data=cancel_tiktaktoe_revansh_cb.new(
                            private_lobby_id = private_lobby_id

            )))
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")

            ))
    return markup