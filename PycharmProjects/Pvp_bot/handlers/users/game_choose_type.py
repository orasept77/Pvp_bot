from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
import aiogram.utils.markdown as fmt

from keyboards.default.game_place_a_bet_menu import place_a_bet_menu
from loader import dp


@dp.message_handler(Text(equals="Когда выбрал сколько фишек хочет просрать", ignore_case=True), state="*")
async def bot_choose_game_type(message: types.Message):
    await message.answer(
        f"Вы выбрали игру *НАЗВАНИЕ ИГРЫ*\n"
        f"Ваш депозит составляет [минус тыща] фишек.\n"
        f"Ваша ставка составляет [миллион] фишек\n\n"
        
        f"Выберите интересующий вас тип игры:\n"
        f"  *Случайный противник - вам будет подобран случайный оппонент.\n"
        f"  *Играть с другом - вы получите уникальный ИД который вы должны будете передать вашему другу.\n"
        f"  *Подключиться к другу - вы должны будете вписать уникальный ИД от вашего друга.\n\n"
        f"Для управления нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=choose_game_type_menu)
