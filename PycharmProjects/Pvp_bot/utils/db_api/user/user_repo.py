from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncpg import Connection

from keyboards.inline.callback_datas import make_a_bet_callback, main_menu_callback, cancel_callback


class UserRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_user(self, user_id):
        sql = 'SELECT * FROM users WHERE id = $1'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def create_user(self, user_id, first_name, last_name, username):
        user = await self.get_user(user_id)
        if not user:
            sql = 'INSERT INTO users (id, first_name, last_name, username) VALUES($1, $2, $3, $4)'
            await self.conn.fetch(sql, user_id, first_name, last_name, username)
            sql = 'INSERT INTO statistics (user_id) VALUES($1)'
            await self.conn.fetch(sql, user_id)
            sql = 'INSERT INTO deposits (user_id) VALUES($1)'
            res = await self.conn.fetch(sql, user_id)
            return res
        else:
            return user

    async def update_user(self, user_id, first_name, last_name, username):
        user = await self.get_user(user_id)
        if not user:
            sql = 'UPDATE users SET first_name = $2, last_name = $3, username = $4 WHERE id = $1'
            res = await self.conn.fetch(sql, user_id, first_name, last_name, username)
            return res
        else:
            return user

    async def set_id(self, user_id, new_id):
        sql = 'UPDATE users SET id = $1 WHERE id = $2'
        res = await self.conn.fetch(sql, user_id, new_id)
        return res

    async def set_name(self, new_name, user_id):
        sql = 'UPDATE users SET name = $1 WHERE id = $2'
        res = await self.conn.fetch(sql, new_name, user_id)
        return res

    async def get_name(self, user_id):
        sql = 'SELECT name FROM users WHERE id = user_id'
        res = await self.conn.fetch(sql, user_id)
        return res

    async def set_chat_id(self, new_chat_id, user_id):
        sql = 'UPDATE users SET chat_id = $1 WHERE id = $2'
        res = await self.conn.fetch(sql, new_chat_id, user_id)
        return res

    async def get_name(self, user_id):
        sql = 'SELECT name FROM users WHERE id = user_id'
        res = await self.conn.fetch(sql, user_id)
        return res