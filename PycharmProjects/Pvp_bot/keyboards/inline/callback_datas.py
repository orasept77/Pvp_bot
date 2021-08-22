  
from aiogram.utils.callback_data import CallbackData

main_menu_callback = CallbackData("main_menu_choice", "menu_choice")
choice_game_callback = CallbackData("game_choice", "game")
choice_game_type_callback = CallbackData("game_type_choice", "game_type")
make_a_bet_callback = CallbackData("player_bet", "id", "bet")
after_game_callback = CallbackData("choice_after_game", "choice")

deposit_main_callback = CallbackData("deposit_menu", "what_to_do")
deposit_deposit_type_callback = CallbackData("deposit", "type")
deposit_deposit_amount_callback = CallbackData("deposit_amount", "amount")
deposit_withdrawal_type_callback = CallbackData("withdrawal", "type")
deposit_withdrawal_amount_callback = CallbackData("withdrawal_amount", "amount")

create_lobby_callback = CallbackData("game_name", "lobby_game_name")
leave_lobby_callback = CallbackData("leave_lobby", "leave")

lobby_ready_callback = CallbackData("lobby_ready", "status")
blackjack_callback = CallbackData("blackjack", "what_to_do")
blackjack_endgame_callback = CallbackData("blackjack_endgame", "result")

tiktaktoe_callback = CallbackData("tiktaktoe_callback", "rates_id")


cancel_callback = CallbackData("cancel_btn", "status")