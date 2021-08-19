from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from games.blackjack.logic import make_decks
from keyboards.inline.callback_datas import create_lobby_callback
from keyboards.inline.game_connect_to_the_friend_menu import connect_to_the_friend_menu
from keyboards.inline.game_place_a_bet_menu import place_a_bet_menu
from loader import dp
from states.start_game import StartGame_State


@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="blackjack"),
                           state=StartGame_State.game)
async def bot_blackjack_first_circle(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.answer(
        f"Вы выбрали игру *НАЗВАНИЕ ИГРЫ*\n"
        f"Ваш депозит составляет [минус тыща] фишек.\n\n"
        f"Выберите наиболее интересующую вас ставку их меню ниже.\n\n"
        f"Для управления депозитом нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=place_a_bet_menu)
    await StartGame_State.type.set()

