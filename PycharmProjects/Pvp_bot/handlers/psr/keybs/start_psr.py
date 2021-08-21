from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
psr_cb = CallbackData("psr_cb", "rates_id", "user_count", "game_type_id")

def start_psr_keyb(rates_id, user_count, game_type_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Старт", callback_data=psr_cb.new(
                            rates_id=rates_id,
                            user_count=user_count,
                            game_type_id=game_type_id

            )))
    markup.add(InlineKeyboardButton(text="Отмена", callback_data=psr_cb.new(
                            rates_id=rates_id,
                            user_count=user_count,
                            game_type_id=game_type_id

            )))
    return markup