# Choice game menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import choice_game_callback, cancel_callback, account_main_callback

cancel_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=account_main_callback.new(
                        enter="true"
                    ))
                ]
            ],
            resize_keyboard=True,
)