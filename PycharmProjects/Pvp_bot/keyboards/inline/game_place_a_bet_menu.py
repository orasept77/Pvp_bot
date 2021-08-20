# Bets menu menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import make_a_bet_callback, main_menu_callback, cancel_callback

place_a_bet_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="5 фишек", callback_data=make_a_bet_callback.new(
                        bet="5"
                    ))
                ],
                [
                    InlineKeyboardButton(text="10 фишек", callback_data=make_a_bet_callback.new(
                        bet="10"
                    )),
                ],
                [
                    InlineKeyboardButton(text="20 фишек", callback_data=make_a_bet_callback.new(
                        bet="20"
                    )),
                ],
                [
                    InlineKeyboardButton(text="⭐ 50 фишек ⭐", callback_data=make_a_bet_callback.new(
                        bet="50"
                    )),
                ],
                [
                    InlineKeyboardButton(text="💰 Депозит 💰", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
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