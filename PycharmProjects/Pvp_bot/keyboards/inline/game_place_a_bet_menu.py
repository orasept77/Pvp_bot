# Bets menu menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import make_a_bet_callback, main_menu_callback, cancel_callback
from utils.db_api.get_bet_list import get_bets_list

bets = get_bets_list()

keyboard = []
for bet in bets:
    keyboard.append([
                    InlineKeyboardButton(text=f"{bet[1]}", callback_data=make_a_bet_callback.new(
                        id=bet[0], bet=f"{bet[1]}"
                    ))
                ])

keyboard.append([
                    InlineKeyboardButton(text="💰 Депозит 💰", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )),
                ])
keyboard.append([
                    InlineKeyboardButton(text="Отмена", callback_data=cancel_callback.new(
                        status="cancel"
                    )),
                ])
place_a_bet_menu = InlineKeyboardMarkup(
            inline_keyboard=keyboard,
            resize_keyboard=True,
)