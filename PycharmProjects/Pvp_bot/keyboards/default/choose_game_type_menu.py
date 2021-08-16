# Deposit menu
from aiogram import types

# --Choose game type menu--
buttons = ["❓ Случайный противник ❓",
           "🤵 Игра с другом 🦹‍♀",
           "🦹‍♀ Подключение к другу 🤵"]
button = types.KeyboardButton(text="🔙 Главное меню 🔙")

choose_game_type_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button)
