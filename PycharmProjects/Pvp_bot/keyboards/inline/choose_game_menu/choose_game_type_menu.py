# Choice game type menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from numpy import result_type

from keyboards.inline.callback_datas import choice_game_type_callback, cancel_callback, main_menu_callback


def choose_game_type_menu_keyb(sup_buttons: list):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="❓   Случайный противник   ❓", callback_data=choice_game_type_callback.new(
                        game_type="random_player"
                    )))
    markup.add(InlineKeyboardButton(text="🤵   Игра с другом   🦹‍♀", callback_data=choice_game_type_callback.new(
                        game_type="play_with_friend"
                    )))
    for i in sup_buttons:
        markup.add(i)
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")))

    return markup