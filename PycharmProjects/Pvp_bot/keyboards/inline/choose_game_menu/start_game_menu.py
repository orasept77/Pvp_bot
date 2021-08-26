from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import create_lobby_callback, cancel_callback, invite_bj_lobby_callback, main_menu_callback

start_blackjack_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="✔   Старт   ✔", callback_data=create_lobby_callback.new(
                        lobby_game_name="blackjack"
                    ))
                ],
                [
                    InlineKeyboardButton(text="❌    Отмена    ❌", callback_data=cancel_callback.new(
                        status="cancel"
                    )),
                ]
            ],
            resize_keyboard=True,
)

invite_blackjack_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="✔   Старт   ✔", callback_data=invite_bj_lobby_callback.new(
                        created="true"
                    ))
                ],
                [
                    InlineKeyboardButton(text="❌    Отмена    ❌", callback_data=cancel_callback.new(
                        status="cancel"
                    )),
                ]
            ],
            resize_keyboard=True,
)

start_rcp_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="✔   Старт   ✔", callback_data=create_lobby_callback.new(
                        lobby_game_name="rcp"
                    ))
                ],
                [
                    InlineKeyboardButton(text="❌   Отмена   ❌", callback_data=cancel_callback.new(
                        status="cancel"
                    )),
                ]
            ],
            resize_keyboard=True,
)



