# Главное сообщение при переходе в меню депозита
# Для редактирования сообщения изменяйте только то, что находится внутри тройных кавычек

async def create_deposit_main_msg(user_deposit):
    return f"""
    
Ваш депозит составляет [{user_deposit[2]}] фишек.
Вы можете пополнить или вывести свой депозит в любое время.

Доступные способы оплаты:
  *LiqPay

Для управления депозитом нажмите на кнопки в меню.

"""