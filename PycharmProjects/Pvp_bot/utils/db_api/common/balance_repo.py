from aiogram.types import user
from asyncpg.connection import Connection

class BalanceRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_rates_by_id(self, rates_id):
        sql = """select * from "rates" where id = $1"""
        return await self.conn.fetchrow(sql, rates_id)

    

    