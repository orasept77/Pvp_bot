# Main menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback, account_statistics_callback, \
    account_update_data_callback, support_callback, account_change_nickname_cb


def account_menu_keyb(sup_btns: list):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="💰   Депозит   💰", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )))
    markup.add(InlineKeyboardButton(text="Статистика игроков", callback_data=account_statistics_callback.new(
                        enter="true"
                    )))
    markup.add(InlineKeyboardButton(text="🔄   Смена кастомного никнейма   🔄", callback_data=account_change_nickname_cb.new(
            change="yes"
        )))
    markup.add(InlineKeyboardButton(text="🔄   Обновить данные профиля   🔄", callback_data=account_update_data_callback.new(
                        enter="true"
                    )))
    markup.add(InlineKeyboardButton(text="📋  Тех. Поддержка  📋", callback_data=support_callback.new(
        to_do="get_info"
    )))
    for i in sup_btns:

        markup.add(i)
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")))
    return markup