from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncpg import Connection

from keyboards.inline.callback_datas import make_a_bet_callback, main_menu_callback, cancel_callback


class StatisticsRepo:
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

    async def get_user_position_blackjack(self, user_id):
        sql = 'SELECT count(*) FROM statistics WHERE win_blackjack < (select win_blackjack from statistics where user_id = $1)'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_user_position_tiktaktoe(self, user_id):
        sql = 'SELECT count(*) FROM statistics WHERE win_tiktaktoe < (select win_tiktaktoe from statistics where user_id = $1)'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_user_position_rpc(self, user_id):
        sql = 'SELECT count(*) FROM statistics WHERE win_rpc < (select win_rpc from statistics where user_id = $1)'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_user_position_balance(self, user_id):
        sql = 'SELECT count(*) FROM statistics WHERE win_balance < (select win_balance from statistics where user_id = $1)'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_games_blackjack(self, user_id):
        sql = 'SELECT games_blackjack FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_win_blackjack(self, user_id):
        sql = 'SELECT win_blackjack FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_top10_win_blackjack(self):
        sql = 'SELECT  u.*, s.* FROM users AS u LEFT JOIN statistics as s ON u.id=s.user_id ORDER BY win_blackjack DESC LIMIT 10'
        res = await self.conn.fetch(sql)
        return res

    async def get_games_tiktaktoe(self, user_id):
        sql = 'SELECT games_tiktaktoe FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_win_tiktaktoe(self, user_id):
        sql = 'SELECT win_tiktaktoe FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_top10_win_tiktaktoe(self):
        sql = 'SELECT  u.*, s.* FROM users AS u LEFT JOIN statistics as s ON u.id=s.user_id ORDER BY win_tiktaktoe DESC LIMIT 10'
        res = await self.conn.fetch(sql)
        return res

    async def get_games_rpc(self, user_id):
        sql = 'SELECT games_rpc FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_win_rpc(self, user_id):
        sql = 'SELECT win_rpc FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_top10_win_rpc(self):
        sql = 'SELECT  u.*, s.* FROM users AS u LEFT JOIN statistics as s ON u.id=s.user_id ORDER BY win_rpc DESC LIMIT 10'
        res = await self.conn.fetch(sql)
        return res

    async def get_win_balance(self, user_id):
        sql = 'SELECT win_balance FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def get_top10_win_balance(self):
        sql = 'SELECT  u.*, s.* FROM users AS u LEFT JOIN statistics as s ON u.id=s.user_id ORDER BY win_balance DESC LIMIT 10'
        res = await self.conn.fetch(sql)
        return res

    async def get_lost_balance(self, user_id):
        sql = 'SELECT lost_balance FROM statistics WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_games_blackjack(self, user_id):
        sql = 'UPDATE statistics SET games_blackjack = win_blackjack + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_win_blackjack(self, user_id):
        sql = 'UPDATE statistics SET win_blackjack = win_blackjack + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_games_tiktaktoe(self, user_id):
        sql = 'UPDATE statistics SET games_tiktaktoe = win_tiktaktoe + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_win_tiktaktoe(self, user_id):
        sql = 'UPDATE statistics SET win_tiktaktoe = win_tiktaktoe + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_games_rpc(self, user_id):
        sql = 'UPDATE statistics SET games_rpc = win_rpc + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_win_rpc(self, user_id):
        sql = 'UPDATE statistics SET win_rpc = win_rpc + 1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def update_lost_balance(self, user_id, balance):
        sql = 'UPDATE statistics SET lost_balance = lost_balance + $1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id, balance)
        return res

    async def update_win_balance(self, user_id, balance):
        sql = 'UPDATE statistics SET win_balance = win_balance + $1 WHERE user_id = $1'
        res = await self.conn.fetch(sql, user_id, balance)
        return res
