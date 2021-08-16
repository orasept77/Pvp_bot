# Main menu
from aiogram import types

buttons = ["❌ Крестики-нолики ⭕",
           "🃏 Блек-джек 🃏",
           "👊 Камень-ножницы-бумага ✂"]
button = types.KeyboardButton(text="💰 Депозит 💰")

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button)
