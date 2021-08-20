from aiogram.utils.callback_data import CallbackData
from aiogram import types

tiktoktoe_make_step_cb = CallbackData('tiktoktoe_make_step_cb', 'cell_id', 'game_id')

def draw(l):
    markup = types.InlineKeyboardMarkup()
    index = 0
    b = []
    for i in l:
        
        if index == 3:
            markup.row(*b)
            b.clear()
            b.append(types.InlineKeyboardButton(i.character, callback_data=tiktoktoe_make_step_cb.new(cell_id=i.cell_id, game_id=i.game_id)))
            index = 1
        else:
            b.append(types.InlineKeyboardButton(i.character, callback_data=tiktoktoe_make_step_cb.new(cell_id=i.cell_id, game_id=i.game_id)))
            index += 1
    if b:
        markup.row(*b)
    return markup