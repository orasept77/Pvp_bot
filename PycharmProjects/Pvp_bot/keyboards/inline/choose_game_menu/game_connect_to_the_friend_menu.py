# Bets menu menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback, cancel_callback

connect_to_the_friend_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="💰   Депозит   💰", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )),
                ],
                [
                    InlineKeyboardButton(text="❌   Отмена   ❌", callback_data=main_menu_callback.new(menu_choice="main_menu")),
                ]
            ],
            resize_keyboard=True,
)