# Choice game menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import cancel_callback

cancel_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="❌   Отмена   ❌", callback_data=cancel_callback.new(
                        status="cancel"
                    )),
                ]
            ],
            resize_keyboard=True,
)