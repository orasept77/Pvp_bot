from aiogram import types
from aiogram.dispatcher import FSMContext
import aiogram.types

from keyboards.inline.callback_datas import create_lobby_callback
from keyboards.inline.choose_game_menu.game_place_a_bet_menu import place_a_bet_menu
from loader import dp
from states.start_game import StartGame_State


@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="tiktaktoe"),
                           state=StartGame_State.game)
async def bot_choice_game(call:aiogram.types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.answer(
        f"Вы выбрали игру *НАЗВАНИЕ ИГРЫ*\n"
        f"Ваш депозит составляет [минус тыща] фишек.\n\n"
        f"Выберите наиболее интересующую вас ставку их меню ниже.\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=place_a_bet_menu)
    await StartGame_State.type.set()



