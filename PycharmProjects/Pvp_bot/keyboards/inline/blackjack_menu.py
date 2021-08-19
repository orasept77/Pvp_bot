# Blackjack menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import blackjack_callback

main_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Взять ещё", callback_data=blackjack_callback.new(
                        what_to_do="more"
                    )),
                    InlineKeyboardButton(text="Хватит", callback_data=blackjack_callback.new(
                        menu_choice="stop"
                    )),
                ]
            ],
            resize_keyboard=True,
)