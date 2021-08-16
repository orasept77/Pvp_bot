from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import aiogram.utils.markdown as fmt

from keyboards.default.game_place_a_bet_menu import place_a_bet_menu
from loader import dp


@dp.message_handler(Text(equals="Выбрал игру я хз как это прописать осталяю временно на вас", ignore_case=True), state="*")
async def bot_place_a_bet(message: types.Message):
    await message.answer(
        f"Вы выбрали игру *НАЗВАНИЕ ИГРЫ*\n"
        f"Ваш депозит составляет [минус тыща] фишек.\n\n"
        f"Выберите наиболее интересующую вас ставку их меню ниже.\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=place_a_bet_menu)
