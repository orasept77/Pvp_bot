from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncpg import Connection

from keyboards.inline.callback_datas import make_a_bet_callback, main_menu_callback, cancel_callback


class RatesRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_rates_list(self):
        sql = 'SELECT * FROM rates'
        res = await self.conn.fetch(sql)
        return res

    async def insert_rates(self):
        sql = 'INSERT INTO rates (value) VALUES (5);'
        await self.conn.fetch(sql)
        sql = 'INSERT INTO rates (value) VALUES (10);'
        await self.conn.fetch(sql)
        sql = 'INSERT INTO rates (value) VALUES (20);'
        await self.conn.fetch(sql)
        sql = 'INSERT INTO rates (value) VALUES (50);'
        await self.conn.fetch(sql)
        return

    async def get_rates_data(self):
        bets = await self.get_rates_list()
        keyboard = []
        for bet in bets:
            keyboard.append([InlineKeyboardButton(text=f"{bet[1]}",
                                                  callback_data=make_a_bet_callback.new(id=bet[0], bet=f"{bet[1]}"))])
        keyboard.append([InlineKeyboardButton(text="💰   Депозит   💰", callback_data=main_menu_callback.new(menu_choice="deposit")), ])
        keyboard.append([InlineKeyboardButton(text="❌   Отмена   ❌", callback_data=cancel_callback.new(status="cancel")), ])
        return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True, )