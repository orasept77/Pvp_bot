
from handlers.psr.keybs.user_count import psr_user_counts
from aiogram.dispatcher.storage import FSMContext
from utils.db_api.psr.psr_repo import PSRRepo
from utils.db_api.create_asyncpg_connection import create_conn
from handlers.psr.keybs.draw import draw
from aiogram.types import CallbackQuery, user
from handlers.psr.keybs.game_types import select_psr_game_type_cb
from handlers.psr.keybs.user_count import select_psr_user_count_cb
from handlers.psr.keybs.start_psr import start_psr_keyb, psr_cb

from loader import dp

@dp.callback_query_handler(select_psr_game_type_cb.filter(), state="*")
async def psr_select_game_type(call:CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    await state.update_data(game_type_id=int(callback_data['id']))
    await state.update_data(game_type_title=callback_data['title'])
    await call.message.edit_text(text="Выберите количество игроков", reply_markup=psr_user_counts([2, 3 ,4]))
    

@dp.callback_query_handler(select_psr_user_count_cb.filter(), state="*")
async def psr_confirm_screen(call:CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    game_name = data['game_name']
    rates_id = data['id']
    rates_value = data['bet']
    user_count = int(callback_data['user_count'])
    game_type_id = data['game_type_id']
    game_type_title = data['game_type_title']
    text = f"Игра: {game_name}\nСтавка: {rates_value}\nРежим игры: {game_type_title}\nКоличество игроков: {user_count}"
    await call.message.edit_text(text=text, reply_markup=start_psr_keyb(rates_id, user_count, game_type_id))


@dp.callback_query_handler(psr_cb.filter(), state="*")
async def start_psr(call:CallbackQuery, callback_data: dict, ):
    rates_id = int(callback_data['rates_id'])
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    players = await repo.get_lobby_players(rates_id, int(callback_data['user_count']))
    if len(players) >= int(callback_data['user_count']) - 1:
        game_id = await repo.create_game(rates_id, int(callback_data['user_count']), int(callback_data['game_type_id']))
        round_id = await repo.add_round(game_id, 1)
        await repo.set_game_round(round_id=round_id, game_id=game_id)
        await repo.add_user_to_game(call.from_user.id, game_id)
        players_ids = [call.from_user.id]
        for i in range(0, int(callback_data['user_count']) - 1):
            await repo.add_user_to_game(players[i]['user_id'], game_id)
            await repo.delete_users_lobby(players[0]['user_id'])
            players_ids.append(players[0]['user_id'])
        variants = await repo.get_variants(int(callback_data['game_type_id']))
        for player_id in players_ids:
            message = await call.message.bot.send_message(chat_id=player_id, text="Раунд 1\nВыберите вариант", reply_markup=draw(variants, game_id))
            await repo.set_game_user_message_id(player_id, game_id, message.message_id)
    else:
        await repo.add_lobby_user(call.from_user.id, rates_id, int(callback_data['user_count']))
    await conn.close()



@dp.callback_query_handler(psr_cb.filter(), state="*")
async def prs_variant_user(call:CallbackQuery, callback_data: dict, ):
    rates_id = int(callback_data['rates_id'])
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    game = await repo.get_game_by_id(int(callback_data['psr_id']))
    if not game['is_end']:
        answer = await repo.get_round_user_variant(game['round_id'], call.from_user.id )
        if answer:
            await call.answer("Вы уже отверили")
            await conn.close()
            return
        else:
            await repo.add_round_user_variant(game['round_id'], int(callback_data['variant_id']), call.from_user.id)
            answers = await repo.get_round_user_variants(game['round_id'])
            if len(answers) == game['user_count']:
                pass