from handlers.psr.keybs.game_types import psr_game_types
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.psr.psr_repo import PSRRepo
from utils.db_api.create_asyncpg_connection import create_conn
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import make_a_bet_callback
from keyboards.inline.choose_game_menu.start_game_menu import start_blackjack_menu, invite_blackjack_menu
from handlers.tiktaktoe.keybs.start_tiktaktoe import start_tiktaktoe

from loader import dp
from states.start_game import StartGame_State


# @dp.callback_query_handler(make_a_bet_callback.filter(bet=["5", "10", "20", "50"]),
#                            state=StartGame_State.bet)
@dp.callback_query_handler(make_a_bet_callback.filter(bet=["5", "10", "20", "50"]))
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    #await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    deposit_repo = DepositRepo(conn=conn)
    user_deposit = await deposit_repo.get_user_deposit(call.from_user.id)
    await state.update_data(id=callback_data.get('id'))
    await state.update_data(bet=callback_data.get('bet'))
    await state.update_data(chat_id=call.message.chat.id)
    data = await state.get_data()
    game_name = data.get('game_name')
    game_type = data.get('type')
    game_bet = data.get('bet')
    await state.finish()
    await state.update_data(**data)
    data = await state.get_data()
    if game_name == 'Блек-Джек':
        if data.get('type') == 'random_player':
            await call.message.edit_text(
                f"Вы выбрали игру {game_name}\n"
                f"Тип игры: случайный соперник\n\n"
                f"Ваш депозит: [{user_deposit[2]}]\n"
                f"Ваша ставка на игру: {game_bet}\n\n"
                f"Для начала игры нажми кнопку 'СТАРТ'.",
                parse_mode=types.ParseMode.HTML, reply_markup=start_blackjack_menu)
        elif data.get('type') == 'play_with_friend':
            await call.message.edit_text(
                f"Вы выбрали игру {game_name}\n"
                f"Тип игры: игра с другом\n\n"
                f"Ваш депозит: [{user_deposit[2]}]\n"
                f"Ваша ставка на игру: {game_bet}\n\n"
                f"Для создания лобби нажми кнопку 'СТАРТ'.",
                parse_mode=types.ParseMode.HTML, reply_markup=invite_blackjack_menu)
    if game_name == 'Крестики-Нолики':
        rates_id = int(callback_data.get('id'))
        await call.message.edit_text(
            f"Вы выбрали игру {game_name}\n"
            f"Тип игры: {game_type}\n"
            f"Ваш депозит: [{user_deposit[2]}]\n"
            f"Ваша ставка на игру: {game_bet}\n\n",
            parse_mode=types.ParseMode.HTML, reply_markup=start_tiktaktoe(rates_id=rates_id))
        return
    if game_name == 'Камень-Ножницы-Бумага':
        conn = await create_conn("conn_str")
        repo = PSRRepo(conn)
        game_types = await repo.get_game_types()
        text = "Выберите режим игры"
        await call.message.edit_text(text=text, reply_markup=psr_game_types(game_types))
        return
    await conn.close()