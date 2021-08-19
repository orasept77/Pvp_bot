# --Choose game type menu--
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import create_lobby_callback

start_blackjack_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Старт", callback_data=create_lobby_callback.new(
                        lobby_game_name="blackjack"
                    ))
                ],
                [
                    InlineKeyboardButton(text="Отмена", callback_data=create_lobby_callback.new(
                        lobby_game_name="blackjack"
                    )),
                ]
            ],
            resize_keyboard=True,
)

start_rcp_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Старт", callback_data=create_lobby_callback.new(
                        lobby_game_name="rcp"
                    ))
                ],
                [
                    InlineKeyboardButton(text="Отмена", callback_data=''),
                ]
            ],
            resize_keyboard=True,
)

start_tiktaktoe_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Старт", callback_data=create_lobby_callback.new(
                        lobby_game_name="tiktaktoe"
                    ))
                ],
                [
                    InlineKeyboardButton(text="Отмена", callback_data=''),
                ]
            ],
            resize_keyboard=True,
)