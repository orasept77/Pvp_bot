from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import create_lobby_callback, cancel_callback, invite_bj_lobby_callback, \
    main_menu_callback, create_private_blackjack_lobby_cb, connect_private_blackjack_lobby_cb

start_blackjack_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="✔   Старт   ✔", callback_data=create_lobby_callback.new(
                        lobby_game_name="blackjack"
                    ))
                ],
                [
                    InlineKeyboardButton(text="❌    Отмена    ❌", callback_data=main_menu_callback.new(menu_choice="main_menu")),
                ]
            ],
            resize_keyboard=True,
)

def play_blackjack_with_friend_keyb():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Создать лобби", callback_data=create_private_blackjack_lobby_cb.new(create_lobby="true")))
    markup.add(InlineKeyboardButton(text="Подключиться", callback_data=connect_private_blackjack_lobby_cb.new(connect_lobby="true")))
    return markup

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



