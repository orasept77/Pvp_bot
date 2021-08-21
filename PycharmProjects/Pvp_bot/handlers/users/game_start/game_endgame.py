from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import CallbackQuery

from keyboards.inline.choose_game_menu.after_game_menu import after_game_menu
from keyboards.inline.callback_datas import cancel_callback
from loader import dp
from states.start_game import StartGame_State


@dp.message_handler(Text(equals="Выбрал игру я хз как это прописать осталяю временно на вас", ignore_case=True), state=None)
async def bot_after_game(message: types.Message):
    await message.answer(
        f"Поздравляем! Вы победили! Или проиграли. Хз логики пока нет\n"
        f"Ваш выигрыш составляет [ноль] фишек.\n\n"
        f"Ваш депозит составляет [минус тыща и плюс ноль] фишек.\n\n"
        f"Вы можете предложить вашему оппоненту реванш "
        f"или сыграть с другим случайным игроком в *НАЗВАНИЕ ИГРЫ*.\n\n"
        f"Для управления нажмите на кнопки в меню.",
        parse_mode=types.ParseMode.HTML, reply_markup=after_game_menu)

@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=StartGame_State.type)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.answer(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()