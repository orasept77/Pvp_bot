from utils.db_api.create_tables_if_not_exists import create_tables_if_not_exists
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


from aiogram import executor
from aiogram.dispatcher.dispatcher import Dispatcher


from loader import dp
import middlewares, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from keyboards.inline.callback_datas import tiktaktoe_callback

import certifi
import urllib3

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)

async def on_startup(dispatcher: Dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    await create_tables_if_not_exists()


if __name__ == '__main__':
    # Запуск телеграм-бота
    executor.start_polling(dp, on_startup=on_startup)
