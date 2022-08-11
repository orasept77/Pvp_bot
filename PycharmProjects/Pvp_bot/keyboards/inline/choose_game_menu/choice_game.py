# Choice game menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import choice_game_callback, cancel_callback, main_menu_callback


def game_choice_menu_keyb(support_buttons: list):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="❌   Крестики-нолики   ⭕", callback_data=choice_game_callback.new(
                        game="Крестики-Нолики"
                    )))
    markup.add(InlineKeyboardButton(text="♠   Блек-джек   ♥", callback_data=choice_game_callback.new(
                        game="Блек-Джек"
                    )))
    markup.add(InlineKeyboardButton(text="✊   Камень-ножницы-бумага   ✌", callback_data=choice_game_callback.new(
                        game="Камень-Ножницы-Бумага"
                    )))
    for btn in support_buttons:
        markup.add(btn)
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")))

    return markup