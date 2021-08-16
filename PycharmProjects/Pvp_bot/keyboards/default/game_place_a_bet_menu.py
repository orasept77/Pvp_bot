# Bet menu
from aiogram import types

buttons = ["5 фишек",
           "10 фишек",
           "20 фишек",
           "⭐ 50 фишек ⭐"]
button = types.KeyboardButton(text="💰 Депозит 💰")

place_a_bet_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button)
