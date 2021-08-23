# Main menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback, account_statistics_callback, \
    account_update_data_callback

def account_menu_keyb(sup_btns: list):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Депозит", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )))
    markup.add(InlineKeyboardButton(text="Статистика игроков", callback_data=account_statistics_callback.new(
                        enter="true"
                    )))
    markup.add(InlineKeyboardButton(text="🔄   Обновить данные профиля   🔄", callback_data=account_update_data_callback.new(
                        enter="true"
                    )))
    markup.add(InlineKeyboardButton(text="🎮  Начать играть  🎮", callback_data=main_menu_callback.new(
                        menu_choice="choice_game"
                    )))
    for i in sup_btns:

        markup.add(i)
    return markup