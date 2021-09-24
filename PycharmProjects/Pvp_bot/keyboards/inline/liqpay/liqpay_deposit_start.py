from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import deposit_main_callback, main_menu_callback, liqpay_deposit_start_callback, \
    liqpay_deposit_stop_callback, liqpay_deposit_data_is_correct_callback

liqpay_deposit_start_menu = InlineKeyboardMarkup(
    inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Старт", callback_data=liqpay_deposit_start_callback.new(
                        start_deposit_liqpay_dialog="start"))
                ],
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=deposit_main_callback.new(
                        what_to_do="withdrawal"))
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,)


liqpay_deposit_data_is_correct = InlineKeyboardMarkup(
    inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Готово", callback_data=liqpay_deposit_data_is_correct_callback.new(correct="true"))
                ],
                [
                    InlineKeyboardButton(text="Отмена", callback_data=liqpay_deposit_stop_callback.new(stop="true"))
                ]
            ],

            resize_keyboard=True,)


liqpay_stop_deposit_state = InlineKeyboardMarkup(
    inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Отмена", callback_data=liqpay_deposit_stop_callback.new(stop="true"))
                ]
            ],
            resize_keyboard=True,)