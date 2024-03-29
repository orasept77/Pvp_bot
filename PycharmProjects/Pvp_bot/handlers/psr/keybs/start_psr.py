from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
from keyboards.inline.callback_datas import main_menu_callback

psr_cb = CallbackData("psr_cb", "rates_id", "user_count", "game_type_id")

psr_revansh_cb = CallbackData("psr_revansh_cb", "private_lobby_id")

cancel_psr_revansh_cb = CallbackData("cancel_psr_revansh_cb", "private_lobby_id")

cancel_psr_randon_cb = "cancel_psr_randon_cb"

create_private_psr_lobby_cb = "create_private_psr_lobby_cb"

connect_private_psr_lobby_cb = "connect_private_psr_lobby_cb"

cancel_psr_private_lobby_cb = CallbackData("cancel_psr_private_lobby_cb", "private_lobby_id")

def start_psr_keyb(rates_id, user_count, game_type_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Старт", callback_data=psr_cb.new(
                            rates_id=rates_id,
                            user_count=user_count,
                            game_type_id=game_type_id

            )))
    markup.add(InlineKeyboardButton(text="Отмена", callback_data=psr_cb.new(
                            rates_id=rates_id,
                            user_count=user_count,
                            game_type_id=game_type_id

            )))
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")))
    return markup

def psr_revansh_keyb(private_lobby_id: int, rates_id, user_count, game_type_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Реванш", callback_data=psr_revansh_cb.new(
                            private_lobby_id = private_lobby_id

            )))
    markup.add(InlineKeyboardButton(text="Играть со случайным игроком", callback_data=psr_cb.new(
                            rates_id=rates_id,
                            user_count=user_count,
                            game_type_id=game_type_id

            )))
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")

            ))
    return markup


def cancel_psr_revansh_keyb(private_lobby_id: int):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Отменить реванш", callback_data=cancel_psr_revansh_cb.new(
                            private_lobby_id = private_lobby_id

            )))
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")

            ))
    return markup

def cancel_psr_random_keyb():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Отменить", callback_data=cancel_psr_randon_cb))
    return markup


def play_psr_with_friend_keyb():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Создать лобби", callback_data=create_private_psr_lobby_cb))
    markup.add(InlineKeyboardButton(text="Подключится", callback_data=connect_private_psr_lobby_cb))
    markup.add(InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu")))
    return markup

def cancel_psr_type_private_lobby_id_keyb():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Отмена", callback_data=main_menu_callback.new(menu_choice="choice_game")))
    return markup   

def cancel_psr_private_lobby_keyb(id):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Покинуть лобби", callback_data=cancel_psr_private_lobby_cb.new(private_lobby_id=id)))
    return markup   
    

