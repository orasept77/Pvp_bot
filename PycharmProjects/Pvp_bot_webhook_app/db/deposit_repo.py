

class DepositRepo:
    def __init__(self, conn):
        self.conn = conn

    def minus_user_deposit(self, user_id, balance):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE deposits SET balance = balance - $2 where user_id = {int(user_id)}"""
        cursor.execute(insert_query)
        self.conn.commit()

    def update_user_deposit(self, user_id, balance):
        cursor = self.conn.cursor()
        insert_query = f"""UPDATE deposits SET balance = balance + $2 where user_id = {int(user_id)}"""
        cursor.execute(insert_query)
        self.conn.commit()