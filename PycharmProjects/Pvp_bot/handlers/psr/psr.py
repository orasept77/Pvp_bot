
from utils.db_api.user.user_repo import UserRepo
from handlers.psr.states.type_private_lobby_id import TypePrivateLobbyId
from aiogram.types.message import Message
from handlers.psr.services.is_eligible_for_next_round import is_eligible_for_next_round
from handlers.psr.models.variant import Variant
from handlers.psr.keybs.user_count import psr_user_counts
from aiogram.dispatcher.storage import FSMContext
from utils.db_api.psr.psr_repo import PSRRepo
from utils.db_api.create_asyncpg_connection import create_conn
from handlers.psr.keybs.draw import draw
from aiogram.types import CallbackQuery, user
from handlers.psr.keybs.game_types import psr_game_types, select_psr_game_type_cb
from handlers.psr.keybs.user_count import select_psr_user_count_cb
from handlers.psr.keybs.start_psr import cancel_psr_private_lobby_cb, cancel_psr_private_lobby_keyb, cancel_psr_type_private_lobby_id_keyb, connect_private_psr_lobby_cb, create_private_psr_lobby_cb, cancel_psr_random_keyb, cancel_psr_revansh_keyb, psr_revansh_keyb, start_psr_keyb, psr_cb, cancel_psr_randon_cb, psr_revansh_cb, cancel_psr_revansh_cb
from handlers.psr.keybs.draw import set_psr_variant_cb
from keyboards.inline.main_menu import to_menu

from loader import dp


@dp.callback_query_handler(lambda call: call.data==create_private_psr_lobby_cb, state="*")
async def create_private_lobby(call:CallbackQuery, state: FSMContext):
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    game_types = await repo.get_game_types()
    text = "Выберите режим игры"
    await call.message.edit_text(text=text, reply_markup=psr_game_types(game_types))
    return


@dp.callback_query_handler(lambda call: call.data==connect_private_psr_lobby_cb, state="*")
async def connect_private_lobby(call:CallbackQuery, state: FSMContext):
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    game_types = await repo.get_game_types()
    text = "Введите идентификатор игры"
    await TypePrivateLobbyId.typing.set()
    await state.update_data(last_message_id=call.message.message_id)
    await call.message.edit_text(text=text, reply_markup=cancel_psr_type_private_lobby_id_keyb())
    return


@dp.message_handler(state=TypePrivateLobbyId.typing)
async def typed_private_lobby_id(message:Message, state: FSMContext):
    conn = await create_conn("conn_str")
    data = await state.get_data()
    repo = PSRRepo(conn)
    if message.text.isnumeric():
        lobby = await repo.get_private_lobby(int(message.text))
        if lobby["is_started"] == True:
            await message.answer("Это лобби уже недоступно", reply_markup=to_menu())
        if lobby:
            players = await repo.get_lobby_private_players(int(message.text))
            if len(players) == lobby['user_count'] - 1:
                user_repo = UserRepo(conn)
                user = await user_repo.get_user(message.from_user.id)
                players.append(user)
                await message.bot.delete_message(message.from_user.id, data.get('last_message_id'))
                await repo.add_private_lobby_user(int(message.text), message.from_user.id)
                await repo.set_private_lobby_started(lobby['id'])
                await create_psr(repo, lobby['rates_id'], lobby['user_count'], players, lobby['game_type_id'], message, 2)
            else:
                await repo.add_private_lobby_user(int(message.text), message.from_user.id)
                await message.answer(text="Вы были добавлены в лобби. Ожидайте остальных игроков", reply_markup=cancel_psr_private_lobby_keyb(lobby['id']))
            await state.finish()
        else:
            await message.answer(text="Игра не найдена. Проверьте правильность ввода цифр.", reply_markup=to_menu())
    else:
        await message.answer(text="Некоректный ввод. Попробуйте еще раз", reply_markup=to_menu())


@dp.callback_query_handler(cancel_psr_private_lobby_cb.filter(), state="*")
async def cancel_psr_private_lobby(call:CallbackQuery, callback_data: dict, state: FSMContext):
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    await repo.delete_private_lobby_user(int(callback_data['private_lobby_id']), call.from_user.id)
    await call.message.edit_text("Вы были удалены из лобби", reply_markup=to_menu())

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
    rates_id = int(data['id'])
    rates_value = data['bet']
    user_count = int(callback_data['user_count'])
    game_type_id = data['game_type_id']
    game_type_title = data['game_type_title']
    text = f"Игра: {game_name}\nСтавка: {rates_value}\nРежим игры: {game_type_title}\nКоличество игроков: {user_count}"
    if data.get('type') == 'random_player':
        await call.message.edit_text(text=text, reply_markup=start_psr_keyb(rates_id, user_count, game_type_id))
    elif data.get('type') == 'play_with_friend':
        conn = await create_conn("conn_str")
        repo = PSRRepo(conn)
        id = await repo.create_private_lobby(user_count, game_type_id, rates_id)
        await repo.add_private_lobby_user(id, call.from_user.id)
        await call.message.edit_text(text=text+"\nИгра создана.\nВы были добавлены в лобби игры.\n<b>Идентификатор игры: {}</b>".format(id), reply_markup=to_menu())


@dp.callback_query_handler(psr_revansh_cb.filter(), state="*")
async def start_psr_revansh(call:CallbackQuery, callback_data: dict, ):
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    lobby = await repo.get_private_lobby(int(callback_data['private_lobby_id']))
    players = await repo.get_lobby_private_players(int(callback_data['private_lobby_id']))
    if len(players) == lobby['user_count'] - 1:
        await repo.add_private_lobby_user(int(callback_data['private_lobby_id']), call.from_user.id)
        user_repo = UserRepo(conn)
        user = await user_repo.get_user(call.from_user.id)
        players.append(user)
        await create_psr(repo, lobby['rates_id'], lobby['user_count'], players, lobby['game_type_id'], call.message, 2)
        await call.message.delete()
    else:
        await repo.add_private_lobby_user(int(callback_data['private_lobby_id']), call.from_user.id)
        await call.answer("Вы записались в очередь на реванш")
        await call.message.edit_text(text=call.message.text, reply_markup=cancel_psr_revansh_keyb(int(callback_data['private_lobby_id'])))
    await conn.close()


@dp.callback_query_handler(cancel_psr_revansh_cb.filter(), state="*")
async def psr_cancel_revansh(call:CallbackQuery, callback_data: dict, ):
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    await repo.delete_private_lobby_user(int(callback_data['private_lobby_id']), call.from_user.id)
    await call.answer("Вы вышли из очереди")
    await call.message.edit_text(text=call.message.text, reply_markup=psr_revansh_keyb(int(callback_data['private_lobby_id'])))


@dp.callback_query_handler(psr_cb.filter(), state="*")
async def start_psr_random(call:CallbackQuery, callback_data: dict, ):
    rates_id = int(callback_data['rates_id'])
    conn = await create_conn("conn_str")
    user_repo = UserRepo(conn)
    user = await user_repo.get_user(call.from_user.id)
    repo = PSRRepo(conn)
    players = await repo.get_lobby_players(rates_id, int(callback_data['user_count']))
    if len(players) >= int(callback_data['user_count']) - 1:
        players.append(user)
        for player in players:
            await repo.delete_users_lobby(player['id'])
        await create_psr(repo, int(callback_data['rates_id']), int(callback_data['user_count']), players, int(callback_data['game_type_id']), call.message, 1)
        await call.message.delete()
    else:
        await repo.add_lobby_user(call.from_user.id, rates_id, int(callback_data['user_count']))
        await call.message.edit_text("Поиск игры начат", reply_markup=cancel_psr_random_keyb())
    await conn.close()

@dp.callback_query_handler(lambda call: call.data == cancel_psr_randon_cb, state="*")
async def cancel_psr_random(call:CallbackQuery ):
    conn = await create_conn("conn_str")
    repo = PSRRepo(conn)
    await repo.delete_users_lobby(call.from_user.id)
    await call.message.edit_text(text="Поиск игры отменен", reply_markup=to_menu())
    await conn.close()


async def create_psr(repo: PSRRepo, rates_id, user_count, players, game_type_id, message: Message, lobby_type_id):
    pl_id = await repo.create_private_lobby(user_count, game_type_id, rates_id)
    game_id = await repo.create_game(rates_id, user_count, game_type_id, pl_id, lobby_type_id)
    round_id = await repo.add_round(game_id, 1)
    await repo.set_game_round(round_id=round_id, game_id=game_id)
    players_text_list = "Игроки:\n"
    for player in players:
        await repo.add_user_to_game(player['id'], game_id)
        await repo.add_round_user(round_id, player['id'])
        players_text_list += player['custom_nick'] + "\n"
    variants = await repo.get_variants(int(game_type_id))
    for player in players:
        message = await message.bot.send_message(chat_id=player['id'], text=players_text_list+"Раунд 1\nВыберите вариант", reply_markup=draw(variants, game_id))
        await repo.set_round_user_message_id(player['id'], round_id, message.message_id)


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
                        text += f"Игрок {answer['custom_nick']}: {answer['variant_title']}\n"
                    text += "\n"
                    if len(winners) > 1:
                        for round_user in round_users:
                            if round_user['user_id'] in winners:
                                result_text = f"Вы проходите в следующий круг. Раунд {game['round_sequence'] + 1}"
                                await repo.add_round_user(round_id, round_user['user_id'])
                                msg = await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+result_text, reply_markup=draw(variants, game['id']))
                                await repo.set_round_user_message_id(round_user['user_id'], round_id, msg.message_id)
                            else:
                                result_text = "Вы не проходите в следующий круг. Для вас игра окончена"
                                await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+result_text, reply_markup=psr_revansh_keyb(game['private_lobby_id']))
                    elif len(winners) == 1:
                        await repo.set_game_end(game['id'])
                        for round_user in round_users:
                            if round_user['user_id'] in winners:
                                await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+"Вы победитель", reply_markup=psr_revansh_keyb(game['private_lobby_id']))
                            else:
                                await call.bot.edit_message_text(chat_id=round_user['user_id'], message_id=round_user['message_id'], text=text+"Вы проиграли", reply_markup=psr_revansh_keyb(game['private_lobby_id']))
                else:
                    await call.message.edit_text(text="Вы дали свой ответ.\nДождитесь ответов всех игроков",)




                    
                