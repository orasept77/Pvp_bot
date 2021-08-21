from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import make_a_bet_callback, cancel_callback
from keyboards.inline.start_game_menu import start_blackjack_menu, start_tiktaktoe, start_rcp_menu
from loader import dp
from states.start_game import StartGame_State


@dp.callback_query_handler(make_a_bet_callback.filter(bet=["5", "10", "20", "50"]),
                           state=StartGame_State.bet)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(bet_id=callback_data.get('id'))
    await state.update_data(bet=callback_data.get('bet'))
    await state.update_data(chat_id=call.message.chat.id)
    data = await state.get_data()
    game_name = data.get('game_name')
    game_type = data.get('type')
    game_bet = data.get('bet')
    if game_name == 'Блек-Джек':
        await call.message.answer(
            f"Вы выбрали игру {game_name}\n"
            f"Тип игры: {game_type}\n"
            f"Ваша ставка на игру: {game_bet}\n\n"
            f"Для начала игры нажми кнопку 'СТАРТ'.",
            parse_mode=types.ParseMode.HTML, reply_markup=start_blackjack_menu)
    if game_name == 'Крестики-Нолики':
        rates_id = int(callback_data.get('bet_id'))
        await call.message.answer(
            f"Вы выбрали игру {game_name}\n"
            f"Тип игры: {game_type}\n"
            f"Ваша ставка на игру: {game_bet}\n\n"
            f"Дальше ничего нет. Нужно писать логику",
            parse_mode=types.ParseMode.HTML, reply_markup=start_tiktaktoe(rates_id=rates_id))
        return
    if game_name == 'Камень-Ножницы-Бумага':
        await call.message.answer(
            f"Вы выбрали игру {game_name}\n"
            f"Тип игры: {game_type}\n"
            f"Ваша ставка на игру: {game_bet}\n\n"
            f"Дальше ничего нет. Нужно писать логику",
            parse_mode=types.ParseMode.HTML, reply_markup=start_rcp_menu)
    await StartGame_State.game.set()
