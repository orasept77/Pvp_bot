# --Choose game type menu--
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import leave_lobby_callback

leave_lobby_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="❌   Покинуть лобби   ❌", callback_data=leave_lobby_callback.new(
                        leave="yes"
                    ))
                ]
            ],
            resize_keyboard=True,
)
