# Choice game menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import choice_game_callback, cancel_callback

game_choice_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="❌ Крестики-нолики ⭕", callback_data=choice_game_callback.new(
                        game="Крестики-Нолики"
                    ))
                ],
                [
                    InlineKeyboardButton(text="🃏 Блек-джек 🃏", callback_data=choice_game_callback.new(
                        game="Блек-Джек"
                    )),
                ],
                [
                    InlineKeyboardButton(text="👊 Камень-ножницы-бумага ✂", callback_data=choice_game_callback.new(
                        game="Камень-Ножницы-Бумага"
                    )),
                ],
                [
                    InlineKeyboardButton(text="Отмена", callback_data=cancel_callback.new(
                        status="cancel"
                    )),
                ]
            ],
            resize_keyboard=True,
)