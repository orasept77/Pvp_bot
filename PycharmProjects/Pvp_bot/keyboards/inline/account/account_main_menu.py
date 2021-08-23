# Main menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback, account_statistics_callback, \
    account_update_data_callback

account_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Депозит", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )),
                    InlineKeyboardButton(text="Статистика игроков", callback_data=account_statistics_callback.new(
                        enter="true"
                    )),
                ],
                [
                    InlineKeyboardButton(text="🔄   Обновить данные профиля   🔄", callback_data=account_update_data_callback.new(
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