from aiogram.dispatcher.filters.state import StatesGroup, State


class StartGame_State(StatesGroup):
    game_name = State()
    type = State()
    bet = State()
