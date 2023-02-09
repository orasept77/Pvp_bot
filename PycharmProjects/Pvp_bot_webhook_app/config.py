# <---      Глобальные настройки приложения         --->
# 'False'  - Статус, когда приложение не в разработке
# 'True' - Статус, когда приложение в разработке
DEBUG = True

# Секретный ключ вашего приложения
SECRET_KEY = ''

# <---      Настройка подключения к базе данных         --->
# Имя пользователя
DB_USER = ""
# Пароль
DB_PASSWORD = ""
# Хост (localhost или IP адресс)
DB_HOST = ""
# Порт
DB_PORT = ""
# Название базы данных
DB_NAME = ""

def return_connection_string():
    return f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
