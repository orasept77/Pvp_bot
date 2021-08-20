
from handlers.tiktaktoe.services.check_winner import check_winner
from utils.db_api.create_asyncpg_connection import create_conn
from handlers.tiktaktoe.models.cell import Cell
from handlers.tiktaktoe.keybs.draw import draw
from utils.db_api.create_connection import db_connection
from utils.db_api.tiktaktoe.tiktaktoe_repo import TikTakToeRepo
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import main_menu_callback
from keyboards.inline.deposit_menu import deposit_menu_main
from loader import dp
from keyboards.inline.callback_datas import tiktaktoe_callback
from handlers.tiktaktoe.keybs.draw import tiktoktoe_make_step_cb


@dp.callback_query_handler(tiktaktoe_callback.filter(), state="*")
async def start_tiktaktoe(call:CallbackQuery, callback_data: dict, ):
    rates_id = int(callback_data['rates_id'])
    conn = await create_conn("conn_str")
    repo = TikTakToeRepo(conn)
    players = await repo.get_lobby_players(rates_id)
    if players:
        game_id = await repo.create_game(rates_id, players[0]['user_id'])
        await repo.delete_users_lobby(players[0]['user_id'])
        await repo.add_user_to_game(players[0]['user_id'], game_id, "X")
        await repo.add_user_to_game(call.from_user.id, game_id, "O")
        await repo.create_cells(9 , game_id)
        charapters = {} 
        charapters[call.from_user.id] = "O"
        charapters[players[0]['user_id']] = "X"
        cells = await repo.get_game_cells(game_id)
        await repo.add_user_steps(9, game_id, user_ids=[players[0]['user_id'], call.from_user.id])
        cells = [Cell(cell['id'], "OPN" if not cell['user_id'] else charapters[cell['user_id']], cell['user_id'], cell['game_id'])  for cell in cells]
        message = await call.message.answer("Вы играете за \"O\"", reply_markup=draw(cells))
        await repo.set_game_user_message_id(call.from_user.id, game_id, message.message_id)
        message = await call.bot.send_message(chat_id=players[0]['user_id'], text="Вы играете за \"X\"", reply_markup=draw(cells))
        await repo.set_game_user_message_id(players[0]['user_id'], game_id, message.message_id)
    else:
        await repo.add_lobby_user(call.from_user.id, rates_id)
    await conn.close()



@dp.callback_query_handler(tiktoktoe_make_step_cb.filter(), state="*")
async def make_step_tiktaktoe(call:CallbackQuery, callback_data: dict):
    conn = await create_conn("conn_str")
    repo = TikTakToeRepo(conn)
    cell = await repo.get_game_cell_by_id(callback_data['cell_id'])
    game = await repo.get_game_by_id(callback_data["game_id"])
    if not game:
        return await call.message.answer("game not found")
    if not cell:
        return await call.message.answer("cell not found")
    if not game['is_end']:
        if game['user_step_id'] != call.from_user.id:
            await call.answer("Сейчас не ваш ход", show_alert=True)
        if not cell['is_busy']:
            await repo.take_cell(call.from_user.id, cell['id'])
            cells = await repo.get_game_cells(game['id'])
            cells = [Cell(cell['id'], "POHUI", cell['user_id'], cell['game_id'])  for cell in cells]
            if_end, winner_id = check_winner(cells)
            if if_end:
                await call.message.answer("игра закончена далее добавляются деньги на баланс а у проигравших отнимаются")
            next_step = await repo.get_step(game['id'], game['step']+1)
            if next_step:
                await repo.set_game_user_step(next_step['sequence'], next_step['user_id'], game['id'])
            game_users = await repo.get_game_users(call.from_user.id, game['id'])
            for game_user in game_users:
                text = "Ход соперника.\nВы играете за {}".format(game_user['character'])
                if game_user.user_id == next_step['user_id']:
                    text = "Ваш Ход.\nВы играете за {}".format(game_user['character'])
                await call.bot.edit_message_text(text=text,
                                                message_id=game_user['message_id'],
                                                chat_id=game_user['user_id'],
                                                reply_markup=draw(cells))
        else:
            await call.answer("Поле уже занято", show_alert=True)
    else:
            await call.answer("Игра уже закончена", show_alert=True)




