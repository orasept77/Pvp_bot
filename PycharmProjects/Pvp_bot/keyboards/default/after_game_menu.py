# Deposit menu
from aiogram import types

# --Choose game type menu--
buttons = ["🏷️ Предложить реванш 🏷️",
           "🤵 Новый соперник 🦹‍♀"]
button = types.KeyboardButton(text="💤 Главное меню 💤")

after_game_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button)
