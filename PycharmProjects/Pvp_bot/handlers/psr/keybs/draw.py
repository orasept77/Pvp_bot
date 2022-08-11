from aiogram.utils.callback_data import CallbackData
from aiogram import types

set_psr_variant_cb = CallbackData('set_psr_variant_cb', 'variant_id', 'psr_id')

def draw(variants: list, psr_id:int):
    markup = types.InlineKeyboardMarkup()
    for i in variants:
        markup.add(types.InlineKeyboardButton(i['title'], callback_data=set_psr_variant_cb.new(variant_id=i['id'], psr_id=psr_id)))
    return markup