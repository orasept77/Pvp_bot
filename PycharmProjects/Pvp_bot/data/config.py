BOT_TOKEN = "1978069005:AAHuzFvxY1-eoCA1DrHdOkqU4DbWN9_9hlI"  # Забираем значение типа str
#BOT_TOKEN = "1820522016:AAGRTSbyFooivgPplZGDdUmmizmN5GqcJjQ"
ADMINS = [462567885]  # Тут у нас будет список из админов
IP = "localhost"  # Тоже str, но для айпи адреса хоста

# <---      Глобальные настройки приложения         --->
# 'False'  - Статус, когда приложение не в разработке
# 'True' - Статус, когда приложение в разработке
DEBUG = True

# Адресс хоста на котором находится сервер
HOST_URL = "yourhost.com"

# Секретный ключ вашего приложения
SECRET_KEY = '123123123'

# Временная зона
TIMEZONE = "UTC"


# <---      Настройка подключения к базе данных         --->
# Имя пользователя
DB_USER = "postgres"
# Пароль
DB_PASSWORD = "123123123"
# Хост (localhost или IP адресс)
DB_HOST = "144.91.110.3"
# Порт
DB_PORT = "5432"
# Название базы данных
DB_NAME = "postgres"


# <---      Настройки модуля LiqPay         --->
# Приватный ключ
LIQPAY_PRIVATEKEY = ''
# Публичный ключ
LIQPAY_PUBLICKEY = ''

# # Ссылка на обработчик платежей оплаты (ввода денег)
# LIQPAY_DEPOSIT_URL = f'{HOST_URL}/webhook_deposits/'
# # Ссылка на обработчик платежей для вывода денег
# LIQPAY_WITHDRAWAL_URL = f'{HOST_URL}/webhook_withdrawals/'

LIQPAY_DEPOSIT_URL = f'{HOST_URL}/webhook_deposits/'
LIQPAY_WITHDRAWAL_URL = f'{HOST_URL}/webhook_withdrawals/'


# Валюта
LIQPAY_CURRENCY = "USD"

# Сообщение, которое увидит пользователь в примечании платежа при успешном выводе
LIQPAY_DEPOSIT_MESSAGE = "Пополнение игрового бота"
# Сообщение, которое увидит пользователь в примечании платежа при успешном выводе
LIQPAY_WITHDRAWAL_MESSAGE = "Вывод средств из игрового бота"


# <---      Настройки для таймеров         --->
# Максимальное количество одновременно запущенных таймеров. Чем выше число - тем больше памяти задействуется
MAX_INSTANCES = 20
# Как часто обновляется таймер. Стандартное значение таймера и частота обновления должны быть кратны
TIMER_TICK = 5
# Общий таймер. Если не приписывать значения для каждого таймера ниже отдельно - то для такого таймера
# будет использоваться время по умолчанию. Для своего значене удалите параметр "DEFAULT_TURN_TIME"
# Значение указывается в секундах (по умолчанию, 120 = 2 минуты)
DEFAULT_TURN_TIME = 120

# Таймер для блекджека
# Времени на ход
BLACKJACK_TURN_TIME = DEFAULT_TURN_TIME

# Таймер для камень-ножницы-бумага
# Времени на ход
TIKTAKTOE_TURN_TIME = DEFAULT_TURN_TIME

# Таймер для крестиков-ноликов
# Времени на ход
RPC_TURN_TIME = DEFAULT_TURN_TIME


# <---      Настройки Блекджека         --->
# Включить/выключить диллера в игре [ True / False ]
BLACKJACK_IS_DEALER_ENABLED = True


# <---      Настройки Крестиков-Ноликов         --->
# Символ незанятой ячейки
TIKTAKTOE_EMPTY_CELL_EMOJI = "☁"

# Символ для первого игрока и его ячейки
TIKTAKTOE_PLAYER_ONE_CELL_EMOJI = "❌"

# Символ для второго игрока и его ячейки
TIKTAKTOE_PLAYER_TWO_CELL_EMOJI = "⭕"