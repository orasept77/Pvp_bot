from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import main_menu_callback
from keyboards.inline.choose_game_menu.choice_game import game_choice_menu
from loader import dp
from states.start_game import StartGame_State


@dp.callback_query_handler(main_menu_callback.filter(menu_choice="choice_game"), state=None)
async def bot_choice_game(call:CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer(
        f"Выберите игру в которую вы бы хотели сыграть",
        parse_mode=types.ParseMode.HTML, reply_markup=game_choice_menu)
    await StartGame_State.game_name.set()

