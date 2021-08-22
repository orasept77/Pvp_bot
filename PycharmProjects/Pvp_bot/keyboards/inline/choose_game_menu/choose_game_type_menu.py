# Choice game type menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import choice_game_type_callback, cancel_callback

choose_game_type_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="❓   Случайный противник   ❓", callback_data=choice_game_type_callback.new(
                        game_type="random_player"
                    ))
                ],
                [
                    InlineKeyboardButton(text="🤵   Игра с другом   🦹‍♀", callback_data=choice_game_type_callback.new(
                        game_type="play_with_friend"
                    )),
                ],
                [
                    InlineKeyboardButton(text="🦹‍♀   Подключение к другу   🤵", callback_data=choice_game_type_callback.new(
                        game_type="connect_to_the_friend"
                    )),
                ],
                [
                    InlineKeyboardButton(text="❌   Отмена   ❌", callback_data=cancel_callback.new(
                        status="cancel"
                    )),
                ]
            ],
            resize_keyboard=True,
)