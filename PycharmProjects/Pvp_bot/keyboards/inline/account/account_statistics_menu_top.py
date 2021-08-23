# Main menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback, account_statistics_callback, \
    account_update_data_callback, account_statistics_top_callback, account_main_callback

account_statistics_menu_top = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Топ блекджека", callback_data=account_statistics_top_callback.new(
                        type="blackjack"
                    )),
                    InlineKeyboardButton(text="Топ камень-ножницы-бумага", callback_data=account_statistics_top_callback.new(
                        type="rpc"
                    ))
                ],
                [
                    InlineKeyboardButton(text="Топ крестики-нолики", callback_data=account_statistics_top_callback.new(
                        type="tiktaktoe"
                    )),
                    InlineKeyboardButton(text="Топ по очкам", callback_data=account_statistics_top_callback.new(
                        type="deposit_win"
                    ))
                ],
                [
                    InlineKeyboardButton(text="🎫  Личный кабинет  🎫", callback_data=account_main_callback.new(
                        enter="true"
                    )),
                ],
                [
                    InlineKeyboardButton(text="🎮  Начать играть  🎮", callback_data=main_menu_callback.new(
                        menu_choice="choice_game"
                    )),
                ]
            ],
            resize_keyboard=True,
)