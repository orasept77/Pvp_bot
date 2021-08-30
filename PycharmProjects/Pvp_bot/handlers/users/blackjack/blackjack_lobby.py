import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.users.blackjack.blackjack import start_blackjack
from keyboards.inline.callback_datas import create_lobby_callback, blackjack_endgame_callback, \
    leave_lobby_callback, invite_bj_lobby_callback, leave_invite_lobby_callback, create_private_blackjack_lobby_cb, \
    connect_private_blackjack_lobby_cb
from keyboards.inline.choose_game_menu.leave_lobby import leave_lobby_menu, leave_invite_lobby_menu
from keyboards.inline.main_menu import to_menu
from loader import dp
from states.blackjack_private_lobby import BlackJackTypePrivateLobbyId
from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn


@dp.callback_query_handler(create_lobby_callback.filter(lobby_game_name="blackjack"))
async def bot_blackjack_create_lobby(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    if data.get('game_id'):
        await repo.delete_game_blackjack(data.get('game_id'))
        await state.update_data(game_id=None)

    data = await state.get_data()
    await state.update_data(chat_id=call.message.chat.id)
    lobby = await repo.find_lobby(data.get('id'))
    if not lobby:
        await repo.create_lobby(call.from_user.id, data.get('id'), call.message.chat.id)
        await call.message.edit_text(
            f"Вы добавленны в лобби. Поиск игроков...\n",
            parse_mode=types.ParseMode.HTML, reply_markup=leave_lobby_menu)
    else:
        await call.message.edit_text(
            f"Мы нашли вам оппонента, скоро игра начнётся!\n",
            parse_mode=types.ParseMode.HTML)
        game = await repo.create_game(data.get('id'))
        await repo.connect_player(call.from_user.id, game[0], call.message.chat.id)
        await repo.connect_player(lobby[0], game[0], lobby[2])
        await repo.delete_lobby_blackjack(lobby[0])
        await start_blackjack(game[0])


@dp.callback_query_handler(create_private_blackjack_lobby_cb.filter(create_lobby="true"))
async def bot_blackjack_create_invite_lobby(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    if data.get('game_id'):
        await repo.delete_game_blackjack(data.get('game_id'))
        await state.update_data(game_id=None)
        data = await state.get_data()
    await state.update_data(chat_id=call.message.chat.id)
    await repo.create_invited_lobby(call.from_user.id, data.get('id'), call.message.chat.id)
    lobby_id = await repo.get_invite_lobby_id(call.from_user.id)
    text = f"Игра: Блекджек\nСтавка:{data.get('bet')}\nИгра создана.\nВы были добавлены в лобби игры.\n\n<b>Идентификатор игры: {str(lobby_id[0])}</b>"
    await call.message.edit_text(
        text=text,
        parse_mode=types.ParseMode.HTML, reply_markup=leave_invite_lobby_menu)
    await conn.close()


@dp.callback_query_handler(connect_private_blackjack_lobby_cb.filter(connect_lobby="true"))
async def bot_blackjack_start_invite_lobby_1(call:CallbackQuery, state: FSMContext):
    text = "Введите идентификатор игры"
    await BlackJackTypePrivateLobbyId.typing.set()
    await state.update_data(last_message_id=call.message.message_id)
    await call.message.edit_text(text=text)


@dp.message_handler(state=BlackJackTypePrivateLobbyId.typing)
async def bot_blackjack_start_invite_lobby(message:Message, state: FSMContext):
    if message.text.isnumeric():
        conn = await create_conn("conn_str")
        repo = BlackJackRepo(conn=conn)
        lobby = await repo.find_invited_lobby(int(message.text))
        if not lobby:
            text = f"Лобби больше не существует или вы ввели неверный номер лобби.\n Для выхода в главное меню используйте меню ниже"
            await message.answer(
                text=text,
                parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
            await conn.close()
            await state.finish()
        else:
            data = await state.get_data()
            if data.get('game_id'):
                await repo.delete_game_blackjack(data.get('game_id'))
                await state.update_data(game_id=None)
                data = await state.get_data()
            await state.update_data(chat_id=message.chat.id)
            await message.answer(
                f"Вы успешно подключились к лобби друга. Игра скоро начнётся!\n",
                parse_mode=types.ParseMode.HTML)
            await state.finish()
            game = await repo.create_game(lobby[2])
            await repo.connect_player(message.from_user.id, game[0], message.chat.id)
            await repo.connect_player(lobby[1], game[0], lobby[3])
            rate = await repo.get_rate_id(game[0])
            await state.update_data(id=rate[0])
            await repo.delete_invite_lobby_by_id(lobby[0])
            await state.update_data(game_id=game[0])
            await state.update_data(user_id=int(message.from_user.id))
            await start_blackjack(game[0])
            await state.finish()
            await conn.close()
    else:
        text = f"Идентификатор должен быть числом!"
        await message.answer(
            text=text,
            parse_mode=types.ParseMode.HTML, reply_markup=to_menu())


@dp.callback_query_handler(blackjack_endgame_callback.filter(result="revenge"))
async def bot_blackjack_revenge(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    await repo.set_player_state(data.get('game_id'), call.from_user.id, 'REVENGE')
    states = await repo.get_players_states(data.get('game_id'))
    if states == None or states == []:
        await call.message.edit_text(
            f"Игрок отказался от реванша. Для доступа к меню используйте команду /start.\n",
            parse_mode=types.ParseMode.HTML, )
    elif states[0][0] == 'REVENGE' and states[1][0] == 'REVENGE' and states != None:
        await call.message.edit_text(
            f"Вы приняли предложение реванша.\n",
            parse_mode=types.ParseMode.HTML)
        await repo.create_revenge_game(data.get('game_id'))
        await start_blackjack(data.get('game_id'))
    else:
        await call.message.edit_text(
            f"Вы отправили предложение реванша. Ожидаем решения игрока.\n",
            parse_mode=types.ParseMode.HTML)
        while states != 'STOP_FIND':
            if states != 'STOP_FIND':
                states = await repo.get_players_states(data.get('game_id'))
            if states != []:
                if (states[0][0] == 'REVENGE' and states[1][0] == 'REVENGE'):
                    states = 'STOP_FIND'
                    extra = 'REVENGE'
            if states == []:
                states = 'STOP_FIND'
                extra = 'bruh'
            await asyncio.sleep(5)
        if states == 'STOP_FIND' and extra != 'REVENGE':
            await call.message.edit_text(
                f"Игрок отказался от реванша.\n",
                parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
    await conn.close()

@dp.callback_query_handler(blackjack_endgame_callback.filter(result="leave"))
async def bot_blackjack_revenge_cancel(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    await repo.delete_game_blackjack(data.get('game_id'))

    await call.message.edit_text(
        f"Вы отменили предложение реванша.\n",
        parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
    await state.finish()
    await conn.close()

@dp.callback_query_handler(leave_lobby_callback.filter(leave="yes"))
async def bot_blackjack_lobby_leave(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    await repo.delete_lobby_blackjack(call.from_user.id)
    await call.message.edit_text(
        f"Вы отменили поиск игры.\n",
        parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
    await state.finish()
    await conn.close()


@dp.callback_query_handler(leave_invite_lobby_callback.filter(leave="true"))
async def bot_blackjack_lobby_invite_leave(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    await repo.delete_invite_lobby_by_userid(call.from_user.id)
    await call.message.edit_text(
        f"Лобби было закрыто.\n",
        parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
    await state.finish()
    await conn.close()


@dp.callback_query_handler(blackjack_endgame_callback.filter(result="leave"))
async def bot_blackjack_game_leave(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    conn = await create_conn("conn_str")
    repo = BlackJackRepo(conn=conn)
    data = await state.get_data()
    await repo.delete_game_blackjack(data.get('game_id'))
    await state.update_data(game_id=None)
    await call.message.edit_text(
        f"Вы покинули игру.\n",
        parse_mode=types.ParseMode.HTML, reply_markup=to_menu())
    await state.finish()
    await conn.close()