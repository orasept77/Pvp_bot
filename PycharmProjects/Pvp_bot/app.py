
from aiogram import executor
from aiogram.dispatcher.dispatcher import Dispatcher

from loader import dp
import middlewares, filters, handlers
from handlers.tiktaktoe.tiktaktoe import start_tiktaktoe
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from keyboards.inline.callback_datas import tiktaktoe_callback

async def on_startup(dispatcher: Dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    dispatcher.register_callback_query_handler(start_tiktaktoe, tiktaktoe_callback.filter(), state="*")
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)