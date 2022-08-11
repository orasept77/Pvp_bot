from aiogram.utils.callback_data import CallbackData
from aiogram import types
from attr import s

select_psr_game_type_cb = CallbackData('select_psr_game_type_cb', 'id', 'title')

def psr_game_types(game_types, support_btns=None):
    markup = types.InlineKeyboardMarkup()
    for i in game_types:
        markup.add(types.InlineKeyboardButton(i['title'], callback_data=select_psr_game_type_cb.new(id=i['id'], title=i['title'])))
    if support_btns:
        for i in support_btns:
            markup.add(i)
    return markup