from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import main_menu_callback
from keyboards.inline.choose_game_menu.choice_game import game_choice_menu_keyb
from loader import dp
from states.start_game import StartGame_State
from aiogram.types import InlineKeyboardButton

@dp.callback_query_handler(main_menu_callback.filter(menu_choice="choice_game"), state="*")
async def bot_choice_game(call:CallbackQuery):
    back_button = InlineKeyboardButton("🔽   Назад   🔽", callback_data=main_menu_callback.new(menu_choice="main_menu"))
    await call.message.edit_text(
        f"Выберите игру в которую вы бы хотели сыграть",
        parse_mode=types.ParseMode.HTML, reply_markup=game_choice_menu_keyb([back_button]))
    #await StartGame_State.game_name.set()

