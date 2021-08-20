from aiogram.utils.callback_data import CallbackData
from aiogram import types

tiktoktoe_make_step_cb = CallbackData('tiktoktoe_make_step_cb', 'cell_id')

def draw(l):
    markup = types.InlineKeyboardMarkup()
    index = 0
    b = []
    for i in l:
        index += 1
        if index % 3 == 0:
            markup.row(*b)
        else:
            b.append(types.InlineKeyboardButton(l['character'], callback_data=tiktoktoe_make_step_cb.new(cell_id=l['cell_id'])))
    if len(b)<3:
        markup.row(*b)
    return markup