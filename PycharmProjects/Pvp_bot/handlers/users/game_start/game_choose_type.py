from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import choice_game_callback, cancel_callback
from keyboards.inline.choose_game_type_menu import choose_game_type_menu
from loader import dp
from states.start_game import StartGame_State


@dp.callback_query_handler(choice_game_callback.filter(game=["Крестики-Нолики", "Блек-Джек", "Камень-Ножницы-Бумага"]),
                           state=StartGame_State.game_name)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(game_name=callback_data.get('game'))
    await state.update_data(user_id=call.from_user.id)
    await call.message.answer(
        f"Вы выбрали игру {callback_data.get('game')}\n"
        f"Ваш депозит составляет [минус тыща] фишек.\n"
        f"Ваша ставка составляет [миллион] фишек\n\n"

        f"Выберите интересующий вас тип игры:\n"
        f"  *Случайный противник - вам будет подобран случайный оппонент.\n"
        f"  *Играть с другом - вы получите уникальный ИД который вы должны будете передать вашему другу.\n"
        f"  *Подключиться к другу - вы должны будете вписать уникальный ИД от вашего друга.\n\n"
        f"Для управления нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=choose_game_type_menu)
    await StartGame_State.type.set()



