from aiogram.types import user
from asyncpg.connection import Connection


class LiqPayRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    # DEPOSITS
    async def create_deposit_order(self, user_id, amount, phone):
        sql = """INSERT INTO liqpay_deposits (user_id, amount, phone, state ) VALUES ($1, $2, $3, $4) RETURNING id"""
        return await self.conn.fetchrow(sql, user_id, amount, phone, 'PROCESSING')

    async def deposit_get_order_user_id(self, order_id):
        sql = """SELECT user_id FROM liqpay_deposits WHERE id = $1"""
        return await self.conn.fetchrow(sql, order_id)

    async def deposit_get_order_amount(self, order_id):
        sql = """SELECT amount FROM liqpay_deposits WHERE id = $1"""
        return await self.conn.fetchrow(sql, order_id)

    async def deposit_order_success(self, order_id):
        sql = """UPDATE liqpay_deposits SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, 'SUCCESS', order_id)

    async def deposit_order_not_enough_money(self, order_id):
        sql = """UPDATE liqpay_deposits SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, 'ERROR:LESS_MONEY', order_id)

    async def deposit_order_error(self, order_id):
        sql = """UPDATE liqpay_deposits SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, 'ERROR', order_id)

    async def deposit_order_set_state(self, order_id, state):
        sql = """UPDATE liqpay_deposits SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, state, order_id)

    # WITHDRAWALS
    async def create_withdrawal_order(self, user_id, amount):
        sql = """INSERT INTO liqpay_withdrawals (user_id, amount, state ) VALUES ($1, $2, $3) RETURNING id"""
        return await self.conn.fetchrow(sql, user_id, int(amount), 'PROCESSING')

    async def withdrawal_get_order_user_id(self, order_id):
        sql = """SELECT user_id FROM liqpay_withdrawals WHERE id = $1"""
        return await self.conn.fetchrow(sql, order_id)

    async def withdrawal_get_order_amount(self, order_id):
        sql = """SELECT amount FROM liqpay_withdrawals WHERE id = $1"""
        return await self.conn.fetchrow(sql, order_id)

    async def withdrawal_set_order_payment_type(self, order_id, payment_type):
        sql = """UPDATE liqpay_withdrawals SET payment_type = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, payment_type, order_id)

    async def withdrawal_set_order_email(self, order_id, email):
        sql = """UPDATE liqpay_withdrawals SET email = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, email, order_id)

    async def withdrawal_set_order_first_name(self, order_id, first_name):
        sql = """UPDATE liqpay_withdrawals SET first_name = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, first_name, order_id)

    async def withdrawal_set_order_last_name(self, order_id, last_name):
        sql = """UPDATE liqpay_withdrawals SET last_name = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, last_name, order_id)

    async def withdrawal_set_order_phone(self, order_id, phone):
        sql = """UPDATE liqpay_withdrawals SET phone = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, phone, order_id)

    async def withdrawal_set_order_card_number(self, order_id, card_number):
        sql = """UPDATE liqpay_withdrawals SET card_number = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, card_number, order_id)

    async def withdrawal_set_order_user_ip(self, order_id, ip):
        sql = """UPDATE liqpay_withdrawals SET ip = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, ip, order_id)

    async def withdrawal_order_success(self, order_id):
        sql = """UPDATE liqpay_withdrawals SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, 'SUCCESS', order_id)

    async def withdrawal_order_failure(self, order_id, state):
        sql = """UPDATE liqpay_withdrawals SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, state, order_id)

    async def withdrawal_order_error(self, order_id):
        sql = """UPDATE liqpay_withdrawals SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, 'DATA IS INCORRECT', order_id)

    async def withdrawal_order_set_state(self, order_id, state):
        sql = """UPDATE liqpay_withdrawals SET state = $1 WHERE id = $2"""
        return await self.conn.fetchrow(sql, state, order_id)
