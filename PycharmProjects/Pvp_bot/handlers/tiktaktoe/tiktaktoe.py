
from handlers.tiktaktoe.models.cell import Cell
from handlers.tiktaktoe.keybs.draw import draw
from utils.db_api.create_connection import db_connection
from utils.db_api.tiktaktoe.tiktaktoe_repo import TikTakToeRepo
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import main_menu_callback
from keyboards.inline.deposit_menu import deposit_menu_main
from loader import dp
from states.deposit import Deposit_State


async def start_tiktaktoe(call:CallbackQuery, callback_data: dict, ):
    rates_id = callback_data['rates_id']
    repo = TikTakToeRepo(db_connection())
    players = await repo.get_lobby_players(rates_id)
    if players:
        game_id = await repo.create_game(rates_id, players[0]['user_id'])
        await repo.delete_users_lobby(players[0]['user_id'])
        await repo.add_user_to_game(players[0]['user_id'], game_id, "X")
        await repo.add_user_to_game(call.from_user.id, game_id, "O")
        await repo.create_cells(9 , game_id)
        charapters = {} 
        ch = await repo.get_user_character(call.from_user.id, game_id)
        if ch:
            charapters[call.from_user.id] = ch
        
        ch = await repo.get_user_character(players[0]['user_id'], game_id)
        if ch:
            charapters[players[0]['user_id']] = ch
        cells = await repo.get_game_cell(game_id)
        cells = [Cell(cell['id'], " " if not cell['user_id'] else charapters[cell['user_id']], cell['user_id'])  for cell in cells]
        await call.message.answer("Вы играете за \"O\"", reply_markup=draw(cells))
        await call.bot.send_message(chat_id=players[0]['user_id'], text="Вы играете за \"X\"", reply_markup=draw(cells))

    