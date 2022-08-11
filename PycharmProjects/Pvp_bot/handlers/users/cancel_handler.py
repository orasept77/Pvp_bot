from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import cancel_callback
from loader import dp
from states.deposit import Deposit_State
from states.start_game import StartGame_State


# GAME HANDLERS
@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=StartGame_State.game_name)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=StartGame_State.type)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=StartGame_State.bet)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(cancel_callback.filter(status='cancel'))
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=StartGame_State.game)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


# DEPOSITS
@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=Deposit_State.what_to_do)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=Deposit_State.amount)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(cancel_callback.filter(status='cancel'),
                           state=Deposit_State.purchase_type)
async def bot_choice_game(call:CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await state.update_data(type=callback_data.get('game_type'))
    await call.message.edit_text(
        f"Отмена\n"
        f"Для доступа в главное меню введите /start\n\n",
        parse_mode=types.ParseMode.HTML)
    await state.finish()