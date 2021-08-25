from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("deposit", "Информация о депозите"),
            types.BotCommand("blackjack_connect_id", "Подключиться к лобби блекджека друга"),
        ]
    )