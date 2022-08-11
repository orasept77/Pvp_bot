from aiogram.utils.callback_data import CallbackData
from aiogram import types


select_psr_user_count_cb = CallbackData('select_psr_user_count_cb', 'user_count')

def psr_user_counts(counts, support_btns=None):
    markup = types.InlineKeyboardMarkup()
    for count in counts:
        markup.add(types.InlineKeyboardButton(str(count), callback_data=select_psr_user_count_cb.new(user_count=count)))
    if support_btns:
        for i in support_btns:
            markup.add(i)
    return markup