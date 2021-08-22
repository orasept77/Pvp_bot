from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncpg import Connection

from keyboards.inline.callback_datas import make_a_bet_callback, main_menu_callback, cancel_callback


class UserRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_stat(self, user_id):
        sql = 'SELECT * FROM statistics WHERE id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def set_stat(self, user_id, win_blackjack, win_tiktaktoe, win_rpc, balance):
        sql = 'UPDATE statistics SET win_blackjack = $1, win_tiktaktoe = $2, win_rpc = $3, balance = $4 WHERE user_id = $5'
        res = await self.conn.fetch(sql, win_blackjack, win_tiktaktoe, win_rpc, balance, user_id)
        return res

    async def get_win_blackjack(self, user_id):
        sql = 'SELECT win_blackjack FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_win_tiktaktoe(self, user_id):
        sql = 'SELECT win_tiktaktoe FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_win_rpc(self, user_id):
        sql = 'SELECT win_rpc FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_win_blackjack(self, user_id):
        sql = 'UPDATE statistics SET win_blackjack = win_blackjack + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_win_tiktaktoe(self, user_id):
        sql = 'UPDATE statistics SET win_tiktaktoe = win_tiktaktoe + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_win_rpc(self, user_id):
        sql = 'UPDATE statistics SET win_rpc = win_rpc + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_balance(self, user_id, balance):
        sql = 'UPDATE statistics SET win_balance = win_balance + $1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id, balance)
        return res
