# --Choose game type menu--
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import lobby_ready_callback

game_ready_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="✔   Начать   ✔", callback_data=lobby_ready_callback.new(
                        status="start"
                    ))
                ],
                [
                    InlineKeyboardButton(text="❌   Отмена   ❌", callback_data=lobby_ready_callback.new(
                        status="abort"
                    )),
                ]
            ],
            resize_keyboard=True,
)
