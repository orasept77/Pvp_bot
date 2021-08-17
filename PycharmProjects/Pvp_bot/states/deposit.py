from aiogram.dispatcher.filters.state import StatesGroup, State


class Deposit_State(StatesGroup):
    what_to_do = State()
    amount = State()
    purchase_type = State()
