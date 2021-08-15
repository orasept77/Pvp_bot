from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = "1931351582:AAG-JYJQeEDheG1pDjnbngLtLF9STyYT7SI"
ADMINS = (573332887,46256788)  # Тут у нас будет список из админов
IP = ("localhost")  # Тоже str, но для айпи адреса хоста
