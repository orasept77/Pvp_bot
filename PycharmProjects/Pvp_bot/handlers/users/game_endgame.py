from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import aiogram.utils.markdown as fmt

from keyboards.default.after_game_menu import after_game_menu
from loader import dp


@dp.message_handler(Text(equals="Выбрал игру я хз как это прописать осталяю временно на вас", ignore_case=True), state="*")
async def bot_after_game(message: types.Message):
    await message.answer(
        f"Поздравляем! Вы победили! Или проиграли. Хз логики пока нет\n"
        f"Ваш выигрыш составляет [ноль] фишек.\n\n"
        f"Ваш депозит составляет [минус тыща и плюс ноль] фишек.\n\n"
        f"Вы можете предложить вашему оппоненту реванш "
        f"или сыграть с другим случайным игроком в *НАЗВАНИЕ ИГРЫ*.\n\n"
        f"Для управления нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=after_game_menu)
