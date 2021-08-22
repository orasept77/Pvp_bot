# --Choose game type menu--
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import after_game_callback

after_game_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="🏷 Предложить реванш 🏷", callback_data=after_game_callback.new(
                        choice="revenge"
                    ))
                ],
                [
                    InlineKeyboardButton(text="🤵 Новый соперник 🦹‍♀", callback_data=after_game_callback.new(
                        choice="random_player"
                    )),
                ],
                [
                    InlineKeyboardButton(text="Отмена", callback_data="cancel"),
                ]
            ],
            resize_keyboard=True,
)