# Choice game menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import account_main_callback, support_task_callback, main_menu_callback

support_menu = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [
                    InlineKeyboardButton(text="Сотрудничество", callback_data=support_task_callback.new(
                        type="сooperation"
                    )),
                ],
                [
                    InlineKeyboardButton(text="Отзывы", callback_data=support_task_callback.new(
                        type="reviews"
                    )),
                ],
                [
                    InlineKeyboardButton(text="Написать про баг", callback_data=support_task_callback.new(
                        type="bug_reply"
                    )),
                ],
                [
                    InlineKeyboardButton(text="Срочная помощь", callback_data=support_task_callback.new(
                        type="urgent_help"
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