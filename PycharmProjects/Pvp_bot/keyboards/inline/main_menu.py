# Main menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback

main_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Выбрать игру", callback_data=main_menu_callback.new(
                        menu_choice="choice_game"
                    )),
                    InlineKeyboardButton(text="Депозит", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )),
                ]
            ],
            resize_keyboard=True,
)
