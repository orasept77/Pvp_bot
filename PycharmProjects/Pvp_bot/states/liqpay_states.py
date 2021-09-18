from aiogram.dispatcher.filters.state import StatesGroup, State


class LiqPayDeposit(StatesGroup):
    typing_phone = State()


# class LiqPayDepositAmount(StatesGroup):
#     typing = State()


class LiqPayWithdrawal(StatesGroup):
    typing_phone = State()
    typing_card = State()
    typing_email = State()
    typing_first_name = State()
    typing_last_name = State()



# class LiqPayWithdrawalAmount(StatesGroup):
#     typing = State()