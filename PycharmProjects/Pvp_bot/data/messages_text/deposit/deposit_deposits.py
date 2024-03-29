# Сообщение, что выводится при нажатии на кнопку "Пополнение"
# Для редактирования сообщения изменяйте только то, что находится внутри тройных кавычек
# {user_deposit[2]} - количество фишек у пользователя
async def create_deposit_choose_amount_msg(user_deposit):
    return f"""
    
Пожалуйста, укажите сумму для пополнения из меню ниже.

На данный момент у вас [{user_deposit[2]}] фишек.

Одна фишка эквивалентна одной гривне ( 1 грн = 1 фишка )

"""


# Сообщение, что выводится когда пользователь решил ввести кастомную сумму для пополнения
# Для редактирования сообщения изменяйте только то, что находится внутри тройных кавычек
async def create_deposit_write_amount_msg():
    return f"""

Введите желаемую сумму для пополнения при помощи клавиатуры.

"""


# Сообщение, что выводится когда пользователь уже выбрал сумму для пополнения и выбирает каким образом ему его пополнить
# Для редактирования сообщения изменяйте только то, что находится внутри тройных кавычек
# {amount} - количество фишек для пополнения
async def create_deposit_choose_type_msg(amount):
    return f"""

Вы выбрали пополнение на {amount} фишек.

Для пополнения депозита выберите предпочитаемый способ получения из меню ниже.

Доступные способы пополнения:
  *LiqPay ( по номеру телефона )

"""


# Сообщение, что выводится когда пользователь уже выбрал сумму для пополнения и выбирает каким образом ему его пополнить
# Для редактирования сообщения изменяйте только то, что находится внутри тройных кавычек
# {amount} - количество фишек для пополнения
async def create_deposit_liqpay_start_msg(amount):
    return f"""

Вы выбрали пополнение через систему LiqPay.
Пополнение на [{amount}] фишек.

Для удачного пополнения, вы должны быть зарегистрированы в услах LiqPay
После ввода номера телефона, вам в Privat24 или любой другой зарегистрированный мессенджер прийдёт уведомление о оплате

Будьте внимательны при предоставлении данных
в случае ошибки при заполнении формы - ваши фишки (и деньги) могут быть утерянны. (но такое происходит крайне редко)
Все данные являются приватными и не передаются третьим лицам.
В случае возникновения каких-либо проблем, пожалуйста напише в службу-поддержки.

Для начала нажмите на кнопку "СТАРТ"

"""
