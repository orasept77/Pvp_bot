  
from aiogram.utils.callback_data import CallbackData

main_menu_callback = CallbackData("main_menu_choice", "menu_choice")
choice_game_callback = CallbackData("game_choice", "game")
choice_game_type_callback = CallbackData("game_type_choice", "game_type")
make_a_bet_callback = CallbackData("player_bet", "id", "bet")
after_game_callback = CallbackData("choice_after_game", "choice")

account_main_callback = CallbackData("account_main", "enter")
account_statistics_callback = CallbackData("account_stat", "enter")
account_statistics_top_callback = CallbackData("account_stat_top", "type")
account_update_data_callback = CallbackData("account_update", "enter")
account_change_nickname_cb = CallbackData("nickname", "change")
account_change_nickname_callback = CallbackData("change_nickname", "button")

support_callback = CallbackData("support", "to_do")
support_task_callback = CallbackData("support_task", "type")
deposit_main_callback = CallbackData("deposit_menu", "what_to_do")
deposit_deposit_type_callback = CallbackData("deposit", "type")
deposit_deposit_amount_callback = CallbackData("deposit_amount", "amount")
deposit_withdrawal_type_callback = CallbackData("withdrawal", "type")
deposit_withdrawal_amount_callback = CallbackData("withdrawal_amount", "amount")

liqpay_deposit_start_callback = CallbackData("liqpay_deposit_start_cb", "start_deposit_liqpay_dialog")
liqpay_deposit_data_is_correct_callback = CallbackData("liqpay_deposit_data_is_correct_callback", "correct")
liqpay_deposit_stop_callback = CallbackData("liqpay_deposit_stop", "stop")

liqpay_withdrawal_starting_dialogue_callback = CallbackData("liqpay_withdrawal_starting_dialogue", "start_withdrawal_dialogue")
liqpay_withdrawal_data_is_correct_callback = CallbackData("liqpay_withdrawal_data_is_correct", "correct")
liqpay_withdrawal_stop_callback = CallbackData("liqpay_withdrawal_stop_callback", "stop")

create_lobby_callback = CallbackData("game_name", "lobby_game_name")
create_private_blackjack_lobby_cb = CallbackData("create_blackjack_lobby", "create_lobby")
connect_private_blackjack_lobby_cb = CallbackData("connect_blackjack_lobby", "connect_lobby")
invite_bj_lobby_callback = CallbackData("lobby", "created")
leave_lobby_callback = CallbackData("leave_lobby", "leave")
leave_invite_lobby_callback = CallbackData("leave_lobby", "leave")

lobby_ready_callback = CallbackData("lobby_ready", "status")
blackjack_callback = CallbackData("blackjack", "what_to_do")
blackjack_endgame_callback = CallbackData("blackjack_endgame", "result")

tiktaktoe_callback = CallbackData("tiktaktoe_callback", "rates_id")


cancel_callback = CallbackData("cancel_btn", "status")
