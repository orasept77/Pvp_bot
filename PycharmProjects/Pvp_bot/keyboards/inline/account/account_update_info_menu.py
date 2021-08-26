# Main menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import main_menu_callback, account_statistics_callback, \
    account_update_data_callback, account_main_callback

account_update_info_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=account_main_callback.new(
                        enter="true"
                    )),
                ],
            ],
            resize_keyboard=True,
)