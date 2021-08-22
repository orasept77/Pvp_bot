from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import aiogram.utils.markdown as fmt
from aiogram.types import CallbackQuery

from keyboards.inline.account.account_statistics_menu_top import account_statistics_menu_top
from keyboards.inline.callback_datas import account_statistics_top_callback, account_statistics_callback
from keyboards.inline.main_menu import main_menu
from loader import dp
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.statistics.statistics_repo import StatisticsRepo
from utils.db_api.user.user_repo import UserRepo


@dp.callback_query_handler(account_statistics_callback.filter(enter="true"))
async def bot_account_statistics(call:CallbackQuery):
    conn = await create_conn("conn_str")
    stat_repo = StatisticsRepo(conn=conn)
    blackjack_games = await stat_repo.get_games_blackjack(call.from_user.id)
    blackjack_wins = await stat_repo.get_win_blackjack(call.from_user.id)
    tiktaktoe_games = await stat_repo.get_games_tiktaktoe(call.from_user.id)
    tiktaktoe_wins = await stat_repo.get_win_tiktaktoe(call.from_user.id)
    rpc_games = await stat_repo.get_games_rpc(call.from_user.id)
    rpc_wins = await stat_repo.get_win_rpc(call.from_user.id)
    deposit_win = await stat_repo.get_win_balance(call.from_user.id)
    deposit_lost = await stat_repo.get_lost_balance(call.from_user.id)
    deposit_position = await stat_repo.get_user_position_balance(call.from_user.id)
    await call.message.answer(
        f"Тут показана ваша статистика по всем сыгранным играм:\n\n"
        f"Блекджек: Игр - {blackjack_games[0][0]} | Побед: {blackjack_wins[0][0]}\n"
        f"Камень-ножницы-бумага: Игр - {rpc_games[0][0]} | Побед: {rpc_wins[0][0]}\n"
        f"Крестики нолики: Игр - {tiktaktoe_games[0][0]} | Побед: {tiktaktoe_wins[0][0]}\n\n"
        f"Всего заработанно очков: {deposit_win[0][0]}\n"
        f"Всего потерянно очков: Игр - {deposit_lost[0][0]}\n"
        f"Вы находитесь на: {deposit_position[0][0]  + 1} месте по количеству заработанных очков.\n\n"
        f"Вы можете изменить статистику начав игру прямо сейчас из меню ниже :)",
        parse_mode=types.ParseMode.HTML, reply_markup=account_statistics_menu_top)
    await conn.close()


@dp.callback_query_handler(account_statistics_top_callback.filter(type="deposit_win"))
async def bot_account_statistics_top_10_by_points(call:CallbackQuery):
    conn = await create_conn("conn_str")
    stat_repo = StatisticsRepo(conn=conn)
    user_top = await stat_repo.get_user_position_balance(call.from_user.id)
    tops = await stat_repo.get_top10_win_balance()
    text=f"Топ 10 игроков по набранным очкам:\nВаша позиция: {user_top[0][0] + 1}\n\n"
    i = 0
    for top in tops:
        text+=f"{i+1}. @{top[3]} - {top[8]}\n"
        i+=i
    await call.message.answer(text,
        parse_mode=types.ParseMode.HTML, reply_markup=account_statistics_menu_top)
    await conn.close()


@dp.callback_query_handler(account_statistics_top_callback.filter(type="blackjack"))
async def bot_account_statistics_top_10_by_win_blackjack(call:CallbackQuery):
    conn = await create_conn("conn_str")
    stat_repo = StatisticsRepo(conn=conn)
    user_top = await stat_repo.get_user_position_balance(call.from_user.id)
    tops = await stat_repo.get_top10_win_blackjack()
    text=f"Топ 10 игроков по победам в блекджек:\nВаша позиция: {user_top[0][0] + 1}\n\n"
    i = 0
    for top in tops:
        text+=f"{i+1}. @{top[3]} - {top[8]}\n"
        i+=i
    await call.message.answer(text,
        parse_mode=types.ParseMode.HTML, reply_markup=account_statistics_menu_top)
    await conn.close()


@dp.callback_query_handler(account_statistics_top_callback.filter(type="tiktaktoe"))
async def bot_account_statistics_top_10_by_win_tiktaktoe(call:CallbackQuery):
    conn = await create_conn("conn_str")
    stat_repo = StatisticsRepo(conn=conn)
    user_top = await stat_repo.get_user_position_balance(call.from_user.id)
    tops = await stat_repo.get_top10_win_tiktaktoe()
    text=f"Топ 10 игроков по победам в крестиках-ноликах:\nВаша позиция: {user_top[0][0] + 1}\n\n"
    i = 0
    for top in tops:
        text+=f"{i+1}. @{top[3]} - {top[8]}\n"
        i+=i
    await call.message.answer(text,
        parse_mode=types.ParseMode.HTML, reply_markup=account_statistics_menu_top)
    await conn.close()


@dp.callback_query_handler(account_statistics_top_callback.filter(type="rpc"))
async def bot_account_statistics_top_10_by_win_rpc(call:CallbackQuery):
    conn = await create_conn("conn_str")
    stat_repo = StatisticsRepo(conn=conn)
    user_top = await stat_repo.get_user_position_balance(call.from_user.id)
    tops = await stat_repo.get_top10_win_rpc()
    text=f"Топ 10 игроков по победам в камень-ножницы-бумага:\nВаша позиция: {user_top[0][0] + 1}\n\n"
    i = 0
    for top in tops:
        text+=f"{i+1}. @{top[3]} - {top[8]}\n"
        i+=i
    await call.message.answer(text,
        parse_mode=types.ParseMode.HTML, reply_markup=account_statistics_menu_top)
    await conn.close()

