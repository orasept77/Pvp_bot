from utils.db_api.user.user_repo import UserRepo
from utils.db_api.common.balance_repo import BalanceRepo
from handlers.tiktaktoe.services.check_winner import check_winner
from utils.db_api.create_asyncpg_connection import create_conn
from handlers.tiktaktoe.models.cell import Cell
from handlers.tiktaktoe.keybs.draw import draw
from utils.db_api.tiktaktoe.tiktaktoe_repo import TikTakToeRepo
from aiogram.types import CallbackQuery
from keyboards.inline.callback_datas import main_menu_callback
from loader import dp
from handlers.tiktaktoe.keybs.start_tiktaktoe import tiktaktoe_callback
from handlers.tiktaktoe.keybs.cancel_search_tiktaktoe import cancel_search_tiktaktoe_cb, cancel_search_tiktaktoe_keyb
from handlers.tiktaktoe.keybs.draw import tiktoktoe_make_step_cb


@dp.callback_query_handler(lambda call: call.data == cancel_search_tiktaktoe_cb, state="*")
async def cancel_search_tiktaktoe(call:CallbackQuery):
    conn = await create_conn("conn_str")
    repo = TikTakToeRepo(conn)
    await repo.delete_users_lobby(call.from_user.id)
    await call.message.answer("Отменено")
    


@dp.callback_query_handler(tiktaktoe_callback.filter(), state="*")
async def start_tiktaktoe_random(call:CallbackQuery, callback_data: dict, ):
    rates_id = int(callback_data['rates_id'])
    conn = await create_conn("conn_str")
    repo = TikTakToeRepo(conn)
    players = await repo.get_lobby_players(rates_id, call.from_user.id)
    if players:
        await repo.delete_users_lobby(players[0]['id'])
        user_repo = UserRepo(conn)
        user = await user_repo.get_user(call.from_user.id)
        players = [players[0], user]
        #await call.message.delete()
        await call.message.answer("Ваша игра найдена")
        await create_tiktaktoe(repo, players, rates_id, call.message)
    else:
        await repo.add_lobby_user(call.from_user.id, rates_id)
        await call.message.answer("Поиск игры начат, для отмены нажмите \"Отменить\" ", reply_markup=cancel_search_tiktaktoe_keyb())
    await conn.close()



async def create_tiktaktoe(repo: TikTakToeRepo, players: list, rates_id: int, message):
    game_id = await repo.create_game(rates_id, players[0]['id'])
    round_id = await repo.create_game_round(game_id, players[0]['id'])
    await repo.create_cells(9 , round_id)
    charapters = {}
    charapters_variants = ["X", "O"]
    for i in range(0, len(players)):
        charapters[players[i]['id']] = charapters_variants[i]
        await repo.add_user_to_game(players[i]['id'], game_id, charapters_variants[i])
        await repo.add_user_to_round(players[i]['id'], round_id, charapters_variants[i])
    cells = await repo.get_game_cells(round_id)
    await repo.add_user_steps(9, round_id, user_ids=[i['id'] for i in players])
    cells = [Cell(cell['id'], "🪑" if not cell['user_id'] else charapters[cell['user_id']], cell['user_id'], cell['round_id'])  for cell in cells]
    for i in players:
        message = await message.bot.send_message(chat_id=i['id'], text=f"Вы играете за {charapters[i['id']]}", reply_markup=draw(cells))
        await repo.set_game_round_user_message_id(i['id'], round_id, message.message_id)






@dp.callback_query_handler(tiktoktoe_make_step_cb.filter(), state="*")
async def make_step_tiktaktoe(call:CallbackQuery, callback_data: dict):
    conn = await create_conn("conn_str")
    repo = TikTakToeRepo(conn)
    cell = await repo.get_round_cell_by_id(int(callback_data['cell_id']))
    round = await repo.get_round_by_id(int(callback_data["round_id"]))
    game = await repo.get_game_by_id(round["game_id"])
    if not game:
        await conn.close()
        return await call.message.answer("game round not found")
    if not cell:
        await conn.close()
        return await call.message.answer("cell not found")
    if not game['is_end']:
        if round['user_step_id'] != call.from_user.id:
            return await call.answer("Сейчас не ваш ход", show_alert=True)
        if not cell['is_busy']:
            game_users = await repo.get_round_users(round['id'])
            await repo.take_cell(call.from_user.id, cell['id'])
            cells: list = await repo.get_game_cells(round['id'])
            cells = [Cell(cell['id'], next((i for i in game_users if i['id'] == cell['user_id']), None)['character'] if cell['user_id'] != None else "🪑" , cell['user_id'], cell['round_id'])  for cell in cells]
            if_end, winner_id = check_winner(cells)
            b_repo = BalanceRepo(conn)
            rates = await b_repo.get_rates_by_id(game['rates_id'])
            if if_end:
                await repo.set_round_end(round['id'])
                await repo.set_round_winner_id(winner_id, round['id'])
                r_w = await repo.get_round_winners(winner_id, game['id'])
                if len(r_w) == 2:
                    text=""
                    await repo.set_game_end(game['id'])
                    r_w = await repo.get_round_winners(winner_id, game['id'])
                    for game_user in game_users:
                        await call.bot.delete_message(chat_id=game_user['id'], message_id=game_user['message_id'])
                        if game_user['id'] == winner_id:
                            await call.bot.send_message(text=f"Вы победили.\nВам было начислено на счет {rates['value']} фишек", chat_id=game_user['id'])
                        else:
                            await call.bot.send_message(text=f"Вы проиграли.\nУ вас было снято со счета {rates['value']} фишек", chat_id=game_user['id'])
                else:
                    round_id = await repo.create_game_round(game['id'], game_users[0]['id'], sequence=round['sequence'] + 1)
                    await repo.create_cells(9 , round_id)
                    charapters = {}
                    charapters_variants = ["X", "O"]
                    for i in range(0, len(game_users)):
                        charapters[game_users[i]['id']] = charapters_variants[i]
                        await repo.add_user_to_round(game_users[i]['id'], round_id, charapters_variants[i])
                    cells = await repo.get_game_cells(round_id)
                    await repo.add_user_steps(9, round_id, user_ids=[i['id'] for i in game_users])
                    cells = [Cell(cell['id'], "🪑" if not cell['user_id'] else charapters[cell['user_id']], cell['user_id'], cell['round_id'])  for cell in cells]
                    for i in game_users:
                        message = await call.message.bot.edit_message_text(chat_id=i['id'],message_id=i['message_id'], text=f"Раунд {round['sequence'] + 1}\n.Вы играете за {charapters[i['id']]}", reply_markup=draw(cells))
                        await repo.set_game_round_user_message_id(i['id'], round_id, message.message_id)
            else:
                next_step = await repo.get_step(round['id'], round['step']+1)
                if next_step:
                    await repo.set_game_round_user_step(next_step['sequence'], next_step['user_id'], round['id'])
                    for game_user in game_users:
                        text = "Раунд: {}.\nХод соперника.\nВы играете за {}".format(round['sequence'],game_user['character'])
                        if game_user['id'] == next_step['user_id']:
                            text = "Раунд: {}.\nВаш Ход.\nВы играете за {}".format(round['sequence'],game_user['character'])
                        await call.bot.edit_message_text(text=text,
                                                    message_id=game_user['message_id'],
                                                    chat_id=game_user['id'],
                                                    reply_markup=draw(cells))
                else:
                    await repo.set_round_end(round['id'])
                    r_w = await repo.get_round_winners(-1, game['id'])
                    if len(r_w) != 1:
                        round_id = await repo.create_game_round(game['id'], game_users[0]['id'], sequence=round['sequence'] + 1)
                        await repo.create_cells(9 , round_id)
                        charapters = {}
                        charapters_variants = ["X", "O"]
                        for i in range(0, len(game_users)):
                            charapters[game_users[i]['id']] = charapters_variants[i]
                            await repo.add_user_to_round(game_users[i]['id'], round_id, charapters_variants[i])
                        cells = await repo.get_game_cells(round_id)
                        await repo.add_user_steps(9, round_id, user_ids=[i['id'] for i in game_users])
                        cells = [Cell(cell['id'], "🪑" if not cell['user_id'] else charapters[cell['user_id']], cell['user_id'], cell['round_id'])  for cell in cells]
                        for i in game_users:
                            message = await call.message.bot.edit_message_text(chat_id=i['id'],message_id=i['message_id'], text=f"Раунд {round['sequence'] + 1}\n.Вы играете за {charapters[i['id']]}", reply_markup=draw(cells))
                            await repo.set_game_round_user_message_id(i['id'], round_id, message.message_id)
                    else:
                        await repo.set_game_end(game['id'])
                        for game_user in game_users:
                            if game_user['id'] == winner_id:
                                await call.bot.send_message(text=f"Вы победили.\nВам было начислено на счет {rates['value']} фишек", chat_id=game_user['id'])
                            else:
                                await call.bot.send_message(text=f"Вы проиграли.\nУ вас было снято со счета {rates['value']} фишек", chat_id=game_user['id'])
        else:
            await call.answer("Поле уже занято", show_alert=True)
    else:
            await call.answer("Игра уже закончена", show_alert=True)
    await conn.close()




