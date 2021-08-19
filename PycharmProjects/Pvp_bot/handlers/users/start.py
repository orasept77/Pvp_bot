from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import aiogram.utils.markdown as fmt

from keyboards.inline.main_menu import main_menu
from loader import dp
from utils.db_api.create_new_user import create_new_user
from utils.db_api.find_room_for_blackjack import find_empty_room_for_blackjack


@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    create_new_user(message.from_user)
    await message.answer(
        f"{fmt.hide_link('https://www.youtube.com/watch?v=dQw4w9WgXcQ')}"
        f"Добро пожаловать в игрового бота *НАЗВАНИЕ БОТА*\n"
        f"У нас вы сможете сыграть в такие замечательные игры, как:\n"
        f"  *Крестики-Нолики.\n  *Блек-джек.\n  *Камень-ножницы-бумага.\n\n"
        f"Мы предоставляем вам возможность бросить вызов другим игрокам и получить за это реальное вознаграждение."
        f"Вам необходимо пополнить Ваш депозит для начала игры и вы сможете бросить вызов любому игроку или своему другу.\n"
        f"Вы выбираете ставку, а затем с кем вы хотите сыграть. Игра идёт до 2х побед.\n\n"
        f"В случае победы - Вы получаете ставку Вашего оппонента, за вычетом нашей скромной комиссии в размере 6%.\n\n"
        f"Вы можете вывести ваш депозит в любой момент времени. 1 фишка приравнивается к 1 гривне.\n\n"
        f"Для проверки состояния вашего депозита - выберите кнопку ''Депозит''\n\n"
        f"Если у вас возникли какие либо вопросы, Мы рекомендуем к просмотру обучающий видео-ролик."
        f"Приятного просмотра и спасибо что выбрали нашего бота :)",
        parse_mode=types.ParseMode.HTML, reply_markup=main_menu)

