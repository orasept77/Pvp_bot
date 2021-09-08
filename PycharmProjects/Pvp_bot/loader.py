import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from psycopg2._psycopg import OperationalError

from data import config
from shedulers.sheduler_config import SchedulerRepo
from utils.db_api.create_connection import db_connection
from utils.db_api.create_tables_if_not_exists import create_tables_if_not_exists

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

scheduler_inst = SchedulerRepo()
scheduler_inst.start_scheduler()
scheduler = scheduler_inst.return_scheduler()
scheduler.start()

create_tables_if_not_exists()