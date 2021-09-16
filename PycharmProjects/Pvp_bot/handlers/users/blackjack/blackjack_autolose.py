import json

from aiogram import types

from keyboards.inline.blackjack_menu.blackjacj_endgame_menu import blackjack_autoloose_menu
from loader import bot

from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.statistics.statistics_repo import StatisticsRepo
from utils.db_api.user.user_repo import UserRepo


async def blackjack_player_auto_loose(player_id):
    conn = await create_conn()
    looser_data = player_id
    repo = BlackJackRepo(conn=conn)
    game_id = await repo.get_player_game_id(int(player_id))
    if game_id is None:
        pass
    else:
        players = await repo.get_players_list_to_announce(game_id['game_id'])
        user_repo = UserRepo(conn=conn)
        stat_repo = StatisticsRepo(conn=conn)
        deposit_repo = DepositRepo(conn=conn)
        rate = await repo.get_rate(game_id['game_id'])
        users_data = []
        i = 0
        for player in players:
            user = await user_repo.get_user(players[i][0])
            if user['id'] == looser_data:
                looser_data = user
                users_data.append(user)
            else:
                users_data.append(user)
            i += 1
        i = 0
        for player in players:
            message_id = await repo.get_player_message_id(player['user_id'], game_id['game_id'])
            chat_id = await repo.get_player_chat_id(player['user_id'], game_id['game_id'])

            if player['user_id'] == looser_data['id']:
                await bot.edit_message_text(chat_id=chat_id['chat_id'], message_id=message_id['message_id'], reply_markup=blackjack_autoloose_menu,
                                       parse_mode=types.ParseMode.HTML, text=
                                       f"У вас истекло время на ход и вы програли из-за отсутствия активности.\n"
                                       f"Вернитесь в главное меню, или сыграйте с новым оппонентом!\n")
                await deposit_repo.minus_user_deposit(looser_data["id"], rate["value"])
                await stat_repo.update_lost_balance(looser_data["id"], rate["value"])
                await stat_repo.update_games_blackjack(looser_data["id"])
            else:
                await bot.edit_message_text(chat_id=chat_id['chat_id'], message_id=message_id['message_id'], reply_markup=blackjack_autoloose_menu,
                                       parse_mode=types.ParseMode.HTML, text=
                                       f"Игрок {users_data[0]['custom_nick']} покинул игру из-за неактивности!\n"
                                       f"Вы победили и получили приз! Выберите нового оппонента для игры из меню ниже.\n")
                await deposit_repo.plus_user_deposit(player["user_id"], rate["value"])
                await stat_repo.update_win_balance(player["user_id"], rate["value"])
                await stat_repo.update_win_blackjack(player["user_id"])
                await stat_repo.update_games_blackjack(player["user_id"])
            i += 1
        await repo.delete_game_blackjack(game_id['game_id'])
    await conn.close()