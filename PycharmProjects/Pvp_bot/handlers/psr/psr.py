
from handlers.psr.services.is_eligible_for_next_round import is_eligible_for_next_round
from handlers.psr.models.variant import Variant
from handlers.psr.keybs.user_count import psr_user_counts
from aiogram.dispatcher.storage import FSMContext
from utils.db_api.psr.psr_repo import PSRRepo
from utils.db_api.create_asyncpg_connection import create_conn
from handlers.psr.keybs.draw import draw
from aiogram.types import CallbackQuery, user
from handlers.psr.keybs.game_types import select_psr_game_type_cb
from handlers.psr.keybs.user_count import select_psr_user_count_cb
from handlers.psr.keybs.start_psr import start_psr_keyb, psr_cb
from handlers.psr.keybs.draw import set_psr_variant_cb

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
    players = await repo.get_lobby_players(rates_id, int(callback_data['user_count']), call.from_user.id)
    if len(players) >= int(callback_data['user_count']) - 1:
        game_id = await repo.create_game(rates_id, int(callback_data['user_count']), int(callback_data['game_type_id']))
        round_id = await repo.add_round(game_id, 1)
        await repo.set_game_round(round_id=round_id, game_id=game_id)
        await repo.add_user_to_game(call.from_user.id, game_id)
        await repo.add_round_user(round_id, call.from_user.id)
        players_ids = [call.from_user.id]
        for i in range(0, int(callback_data['user_count']) - 1):
            await repo.add_user_to_game(players[i]['user_id'], game_id)
            await repo.add_round_user(round_id, players[i]['user_id'])
            await repo.delete_users_lobby(players[i]['user_id'])
            players_ids.append(players[i]['user_id'])
        variants = await repo.get_variants(int(callback_data['game_type_id']))
        for player_id in players_ids:
            message = await call.message.bot.send_message(chat_id=player_id, text="Раунд 1\nВыберите вариант", reply_markup=draw(variants, game_id))
            await repo.set_round_user_message_id(player_id, round_id, message.message_id)
    else:
        await repo.add_lobby_user(call.from_user.id, rates_id, int(callback_data['user_count']))
    await conn.close()



@dp.callback_query_handler(set_psr_variant_cb.filter(), state="*")
async def prs_variant_user(call:CallbackQuery, callback_data: dict, ):
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    game = await repo.get_game_by_id(int(callback_data['psr_id']))
    if game and not game['is_end']:
        round_users = await repo.get_round_users(game['round_id'])
        if call.from_user.id in [round_user['user_id'] for round_user in round_users]:
            answer = await repo.get_round_user_variant(call.from_user.id, game['round_id'])
            if answer:
                await call.answer("Вы уже ответили")
                await conn.close()
                return
            else:
                await repo.add_round_user_variant(game['round_id'], int(callback_data['variant_id']), call.from_user.id)
                answers = await repo.get_round_user_variants(game['round_id'])
                if len(answers) == len(round_users):
                    round_id = await repo.add_round(game['id'], game['round_sequence'] + 1)
                    await repo.set_game_round(round_id=round_id, game_id=game['id'])
                    variants = await repo.get_variants(game['game_type_id'])
                    variants_models = []
                    for variant in variants:
                        bvariants = await repo.get_beaten_variants(variant['id'])
                        variants_models.append(Variant(variant['id'], variant['title'], [Variant(bvariant['id'], bvariant['title'], []) for bvariant in bvariants] ))
                    if_end, winners = is_eligible_for_next_round(variants_models, answers)
                    text = "Ответы игроков прошлого раунда:\n"
                    for answer in answers:
                        text += f"Игрок {answer['user_name']}: {answer['variant_title']}\n"
                    text += "\n"
                    if len(winners) > 1:
                        for round_user in round_users:
                            if round_user['user_id'] in winners:
                                result_text = "Вы проходите в следующий круг"
                                await repo.add_round_user(round_id, round_user['user_id'])
                                msg = await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+result_text, reply_markup=draw(variants, game['id']))
                                await repo.set_round_user_message_id(round_user['user_id'], round_id, msg.message_id)
                            else:
                                result_text = "Вы не проходите в следующий круг. Для вас игра окончена"
                                await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+result_text)
                    elif len(winners) == 1:
                        await repo.set_game_end(game['id'])
                        for round_user in round_users:
                            if round_user['user_id'] in winners:
                                await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+"Вы победитель")
                            else:
                                await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+"Вы проиграли")
                    """ if winners:
                    user_index = 1
                    for winner in winners:
                        await repo.add_round_user(round_id, winner)
                        if winner != call.from_user.id:
                            text += f"Игрок {user_index} ответил:"
                        variant = "unknown"
                        a = next((answer for answer in answers if answer['user_id'] == winner), None)
                        if a:
                            variant = a["variant_title"]
                        text += variant + "\n"
                    for winner in winners:
                        user = next((i for i in round_users if i['user_id'] == winner))
                        await call.message.edit_text(chat_id=winner, message_id=user['message_id'], text=text+"Вы проходите в следующий круг\n")
                    """





                    
                