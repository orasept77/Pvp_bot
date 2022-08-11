# <---      Глобальные настройки приложения         --->
# 'False'  - Статус, когда приложение не в разработке
# 'True' - Статус, когда приложение в разработке
DEBUG = True

# Секретный ключ вашего приложения
SECRET_KEY = '123123123'

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

def return_connection_string():
    return f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"