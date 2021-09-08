# Blackjack menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import blackjack_endgame_callback, cancel_callback, create_lobby_callback

blackjack_endgame_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Реванш", callback_data=blackjack_endgame_callback.new(
                        result="revenge"
                    )),
                ],
                [

                    InlineKeyboardButton(text="Играть со случайным игроком", callback_data=create_lobby_callback.new(
                        lobby_game_name="blackjack"
                    )),
                ],
                [
                    InlineKeyboardButton(text="❌   Выход   ❌", callback_data=blackjack_endgame_callback.new(
                        result="leave"
                    ))
                ]
            ],
            resize_keyboard=True,
)

blackjack_autoloose_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Играть со случайным игроком", callback_data=create_lobby_callback.new(
                        lobby_game_name="blackjack"
                    )),
                ],
                [
                    InlineKeyboardButton(text="❌   Выход   ❌", callback_data=blackjack_endgame_callback.new(
                        result="leave"
                    ))
                ]
            ],
            resize_keyboard=True,
)