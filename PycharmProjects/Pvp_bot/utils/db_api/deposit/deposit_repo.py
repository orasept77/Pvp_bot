from aiogram.types import user
from asyncpg.connection import Connection


class DepositRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_user_deposit(self, user_id):
        sql = """select * from deposits where user_id = $1"""
        return await self.conn.fetchrow(sql, user_id)

    async def plus_user_deposit(self, user_id, balance):
        sql = """UPDATE deposits SET balance = balance + $2 where user_id = $1"""
        return await self.conn.fetchrow(sql, user_id, balance)

    async def minus_user_deposit(self, user_id, balance):
        sql = """UPDATE deposits SET balance = balance - $2 where user_id = $1"""
        return await self.conn.fetchrow(sql, user_id, balance)



