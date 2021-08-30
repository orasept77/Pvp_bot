# Main menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback, account_statistics_callback, \
    account_update_data_callback, support_callback, account_change_nickname_callback, account_main_callback


def account_change_nickname_keyb():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Да", callback_data=account_change_nickname_callback.new(
                        button="yes"
                    )))
    markup.add(InlineKeyboardButton(text="Нет", callback_data=account_main_callback.new(
                        enter="true"
                    )))
    return markup