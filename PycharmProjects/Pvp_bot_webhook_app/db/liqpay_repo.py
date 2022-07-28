

class LiqPayRepo:
    def __init__(self, conn):
        self.conn = conn

    def deposit_get_user(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT user_id FROM liqpay_deposits where id = {id}")
        record = cursor.fetchone()
        return record

    def deposit_get_amount(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT amount FROM liqpay_deposits where id = {id}")
        record = cursor.fetchone()
        return record

    def withdrawal_get_user(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT user_id FROM liqpay_withdrawals where id = {id}")
        record = cursor.fetchone()
        return record

    def deposit_set_bot_channel(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET bot_channel = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_bot_in_contacts(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET bot_in_contacts = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_bot_name(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET bot_name = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_bot_url(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET bot_url = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_href(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET href = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_id(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET id_trans = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_result(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET result = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_token(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET token = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def deposit_set_state(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE liqpay_deposits SET state  = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()



    def withdrawal_set_payment_type(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET payment_type = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_amount(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET amount = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_ip(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET ip = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_card_number(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET card_number = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_phone(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET phone = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_payment_type(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET payment_type = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_first_name(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET first_name = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_last_name(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET last_name = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_status(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET status = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_description(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET description = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_state(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET state = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_create_date(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET create_date = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_end_date(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET end_date = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_acq_id(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET acq_id = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_action(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET action = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_payment_type(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET payment_type = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_agent_commission(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET agent_commission = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_amount_bonus(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET amount_bonus = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_amount_credit(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET amount_credit = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_amount_debit(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET amount_debit = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_commission_credit(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET commission_credit = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_commission_debit(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET commission_debit = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_currency(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET currency = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_currency_credit(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET currency_credit = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_currency_debit(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET currency_debit = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_is_3ds(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET is_3ds = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_liqpay_order_id(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET liqpay_order_id = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_mpi_eci(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET mpi_eci = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_payment_id(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET payment_id = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_receiver_commission(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET receiver_commission = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_redirect_to(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET redirect_to = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_sender_bonus(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET sender_bonus = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_sender_commission(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET sender_commission = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_transaction_id(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET transaction_id = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def withdrawal_set_type(self, id, value):
        cursor = self.conn.cursor()
        insert_query = f""" UPDATE liqpay_withdrawals SET type = "{value}") WHERE id = {id}"""
        cursor.execute(insert_query)
        self.conn.commit()