# Deposit menu
from aiogram import types

# --Main deposit menu--
buttons = ["❌ Пополнить ⭕",
           "🃏 Вывести 🃏"]
button = types.KeyboardButton(text="🔙 Главное меню 🔙")

deposit_menu_main = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button)


# --Withdrawal deposit menu--
buttons = ["💳 Вывести на карту (Приватбанк) 💳"]
button = types.KeyboardButton(text="🔙 Главное меню 🔙")

withdrawal_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button)


# --Make a deposit menu--
buttons = ["💳 Пополнить картой (Приватбанк) 💳"]
button = types.KeyboardButton(text="🔙 Главное меню 🔙")

deposit_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button)


# --Deposit amount menu--
buttons = ["50 фишек",
           "100 фишек",
           "200 фишек",
           "⭐ 500 фишек ⭐",]
button = types.KeyboardButton(text="Другая сумма")
button2 = types.KeyboardButton(text="🔙 Главное меню 🔙")

deposit_amount_menu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, button, button2)