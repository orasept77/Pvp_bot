# Deposit menu
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import deposit_main_callback, deposit_deposit_type_callback, \
    deposit_withdrawal_type_callback, deposit_deposit_amount_callback, deposit_withdrawal_amount_callback, \
    cancel_callback, account_main_callback, main_menu_callback

# --Main deposit menu--
deposit_menu_main = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="💳   Пополнить   💳", callback_data=deposit_main_callback.new(
                        what_to_do="deposit"
                    ))
                ],
                [
                    InlineKeyboardButton(text="🃏   Вывести   🃏", callback_data=deposit_main_callback.new(
                        what_to_do="withdrawal"
                    )),
                ],
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=account_main_callback.new(
                        enter="true"
                    )),
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)

# --Withdrawal deposit menu--
withdrawal_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="💳   Вывести на карту (Приватбанк)   💳", callback_data=deposit_withdrawal_type_callback.new(
                        type="card_privatbank"
                    ))
                ],
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=deposit_main_callback.new(
                        what_to_do="withdrawal"
                    ))
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)

# --Make a deposit menu--
deposit_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="💳   Пополнить картой (Приватбанк)   💳", callback_data=deposit_deposit_type_callback.new(
                        type="card_privatbank"
                    ))
                ],
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=deposit_main_callback.new(
                        what_to_do="deposit"
                    )),
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)

# --Deposit amount menu--
deposit_amount_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="50 фишек", callback_data=deposit_deposit_amount_callback.new(
                        amount="50"
                    ))
                ],
                [
                    InlineKeyboardButton(text="100 фишек", callback_data=deposit_deposit_amount_callback.new(
                        amount="100"
                    )),
                ],
                [
                    InlineKeyboardButton(text="200 фишек", callback_data=deposit_deposit_amount_callback.new(
                        amount="200"
                    ))
                ],
                [
                    InlineKeyboardButton(text="⭐   500 фишек   ⭐", callback_data=deposit_deposit_amount_callback.new(
                        amount="500"
                    )),
                ],
                [
                    InlineKeyboardButton(text="✒   Другая сумма   ✒", callback_data=deposit_deposit_amount_callback.new(
                        amount="another"
                    )),
                ],
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )),
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)


# --Withdrawal amount menu--
withdrawal_amount_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="50 фишек", callback_data=deposit_withdrawal_amount_callback.new(
                        amount="50"
                    ))
                ],
                [
                    InlineKeyboardButton(text="100 фишек", callback_data=deposit_withdrawal_amount_callback.new(
                        amount="100"
                    )),
                ],
                [
                    InlineKeyboardButton(text="200 фишек", callback_data=deposit_withdrawal_amount_callback.new(
                        amount="200"
                    ))
                ],
                [
                    InlineKeyboardButton(text="⭐   500 фишек   ⭐", callback_data=deposit_withdrawal_amount_callback.new(
                        amount="500"
                    )),
                ],
                [
                    InlineKeyboardButton(text="✒   Другая сумма   ✒", callback_data=deposit_withdrawal_amount_callback.new(
                        amount="another"
                    )),
                ],
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=main_menu_callback.new(
                        menu_choice="deposit"
                    )),
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)
deposit_amount_back_menu = InlineKeyboardMarkup(
    inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=deposit_main_callback.new(
                        what_to_do="deposit"
                    ))
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)

withdrawal_amount_back_menu = InlineKeyboardMarkup(
    inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=deposit_main_callback.new(
                        what_to_do="withdrawal"
                    ))
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)

withdrawal_type_back_menu = InlineKeyboardMarkup(
    inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=deposit_main_callback.new(
                        what_to_do="withdrawal"
                    ))
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)

deposit_type_back_menu = InlineKeyboardMarkup(
    inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="🔽   Назад   🔽", callback_data=deposit_main_callback.new(
                        what_to_do="deposit"
                    ))
                ],
                [
                    InlineKeyboardButton(text="В меню", callback_data=main_menu_callback.new(menu_choice="main_menu"))
                ]
            ],
            resize_keyboard=True,
)