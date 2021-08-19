import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

from logic import make_decks, total_up

card_types = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
blackjack = set(['A', 10])


# Указываем количество игроков
def set_nubmer_of_players(players_count: int):
    return players_count


# Сбрасываем руку дилера
def empty_hand():
    return []


# Выдать карту игроку
def give_card(deck, hand):
    hand.append(deck.pop(0))


# Получение первых двух карт
def give_first_cards(deck, player_one_hand, player_two_hand, dealer_hand):
    # Получение ПЕРВОЙ карты
    give_card(deck, player_one_hand)
    give_card(deck, player_two_hand)
    give_card(deck, dealer_hand)
    # Получение ВТОРОЙ карты
    give_card(deck, player_one_hand)
    give_card(deck, player_two_hand)
    give_card(deck, dealer_hand)


# Дилер и игроки проверяются на 21
def check_blackjack(hand):
    if set(hand) == blackjack:
        return True


# Проверка на перебор (больше 21 очка в руке)
def more_than_21(hand):
    if total_up(hand) > 21:
        return True


# Дилер добирает карты, если сумма его очков меньше 17ти
def dealer_take_card_if_totalup_less_17(deck, dealer_hand):
    while total_up(dealer_hand) < 17:
        dealer_hand.append(deck.pop(0))


# Сравнение рук игроков
def compare_players_hands(player_one_hand, player_two_hand):
    if total_up(player_one_hand) > total_up(player_two_hand) and total_up(player_one_hand) <= 21:
        print('у игрока 1 <= 21, и при этом у игрока 1 > чем у игрока 2')
        return 'player_one_won'
    elif total_up(player_one_hand) < total_up(player_two_hand) and total_up(player_two_hand) <= 21:
        print('у игрока 2 <= 21, и при этом у игрока 1 > чем у игрока 2')
        return 'player_two_won'
    elif total_up(player_one_hand) == total_up(player_two_hand) and total_up(player_one_hand) <= 21:
        print('у игроков одинаковое количество очков и меньше 21го')
        return 'draw'
    elif total_up(player_one_hand) == total_up(player_two_hand) and more_than_21(player_one_hand):
        print('у игроков одинаковое количество очков и больше 21го')
        return 'draw_more_21'
    elif more_than_21(player_one_hand) and not more_than_21(player_two_hand):
        print('у игрока 1 > 21, а игрока 2 < 21')
        return 'player_two_won'
    elif more_than_21(player_two_hand) and not more_than_21(player_one_hand):
        print('у игрока 2 > 21, а игрока 1 < 21')
        return 'player_one_won'
    elif more_than_21(player_two_hand) and more_than_21(player_one_hand):
        print('у обоих больше 21')
        return 'draw_more_21'
    else:
        print('UNEXPECTED_RESULT')
        return 'UNEXPECTED_RESULT'


# Сравнение рук игроков и дилера
def compare_players_with_dealer_hands(dealer_hand, player_one_hand, player_two_hand, result):
    if result == 'player_one_won' and more_than_21(dealer_hand):
        print('игрок 1 выиграл, и у дилера больше 21')
        return 'player_one_won'
    elif result == 'player_one_won' and total_up(dealer_hand) <= 21 and total_up(dealer_hand) < total_up(player_one_hand):
        print('у игрока 1 больше чем у дилера, и у дилера меньше 21')
        return 'player_one_won'
    elif result == 'player_one_won' and total_up(dealer_hand) <= 21 and total_up(dealer_hand) > total_up(player_one_hand):
        print('у игрока 1 меньше чем у дилера, и у дилера меньше 21')
        return 'dealer_won'
    elif result == 'player_one_won' and total_up(dealer_hand) <= 21 and total_up(dealer_hand) == total_up(player_one_hand):
        print('у игрока 1 и дилера одинаковый результат')
        return 'draw'

    elif result == 'player_two_won' and more_than_21(dealer_hand):
        print('игрок 2 выиграл, и у дилера больше 21')
        return 'player_two_won'
    elif result == 'player_two_won' and total_up(dealer_hand) <= 21 and total_up(dealer_hand) < total_up(player_two_hand):
        print('у игрока 2 больше чем у дилера, и у дилера меньше 21')
        return 'player_two_won'
    elif result == 'player_two_won' and total_up(dealer_hand) <= 21 and total_up(dealer_hand) > total_up(player_two_hand):
        print('у игрока 2 меньше чем у дилера, и у дилера меньше 21')
        return 'dealer_won'
    elif result == 'player_two_won' and total_up(dealer_hand) <= 21 and total_up(dealer_hand) == total_up(player_two_hand):
        print('у игрока 2 и дилера одинаковый результат')
        return 'draw'

    elif result == 'draw_more_21' and total_up(dealer_hand) <= 21:
        print('у игроков больше 21, а у дилера меньше 21')
        return 'dealer_won'
    elif result == 'draw_more_21' and more_than_21(dealer_hand):
        print('у игроков и у дилера больше 21')
        return 'draw'

    elif result == 'draw' and more_than_21(dealer_hand):
        print('у игроков одинаковое кол-во очков, а у дилера больше 21')
        return 'draw'
    elif result == 'draw' and total_up(player_one_hand) > total_up(dealer_hand) and total_up(dealer_hand) <=21:
        print('у игроков одинаковое кол-во очков и больше чем у дилера, а у дилера меньше 21')
        return 'draw'
    elif result == 'draw' and total_up(player_one_hand) < total_up(dealer_hand) and total_up(dealer_hand) <=21:
        print('у игроков одинаковое кол-во очков но меньше чем у дилера, а у дилера меньше 21')
        return 'dealer_won'
    elif result == 'draw' and total_up(player_one_hand) == total_up(dealer_hand):
        print('у всех одинаковое количество очков')
        return 'draw'


# TESTS
result = 'Null'
print(f"Результаты игроков: {result}")  #
deck = make_decks(1, card_types)        #
print(f"Начальная колода: {deck}")      #

# Рука дилела
dealer_hand = empty_hand()
player_one_hand = empty_hand()
player_two_hand = empty_hand()
print(f"Рука дилера: {dealer_hand}, {total_up(dealer_hand)}")
print(f"Рука игрока 1: {player_one_hand}, {total_up(player_one_hand)}")
print(f"Рука игрока 2: {player_two_hand}, {total_up(player_two_hand)}")
print()

# Начинается игра
print("Начало игры")
give_first_cards(deck, player_one_hand, player_two_hand, dealer_hand)
print("Раздали первые 2 карты. Руки игроков:")
print(f"Рука дилера: {dealer_hand}, {total_up(dealer_hand)}")
print(f"Рука игрока 1: {player_one_hand}, {total_up(player_one_hand)}")
print(f"Рука игрока 2: {player_two_hand}, {total_up(player_two_hand)}")
print(f"Колода: {deck}")
print()

give_card(deck, player_one_hand)
give_card(deck, player_two_hand)
print("Игроки 1 и 2 взяли по 1 карте")
print(f"Рука игрока 1: {player_one_hand}, {total_up(player_one_hand)}")
print(f"Рука игрока 2: {player_two_hand}, {total_up(player_two_hand)}")
print(f"Колода: {deck}")
print()

# give_card(deck, player_one_hand)
# give_card(deck, player_two_hand)
# print("Игроки 1 и 2 взяли по 1 карте")
# print(f"Рука игрока 1: {player_one_hand}, {total_up(player_one_hand)}")
# print(f"Рука игрока 2: {player_two_hand}, {total_up(player_two_hand)}")
# print(f"Колода: {deck}")
# print()

print(f"Рука дилера: {dealer_hand}, {total_up(dealer_hand)}")
dealer_take_card_if_totalup_less_17(deck, dealer_hand)
print("Если у дилера меньше 17 он добирает карты:")
print(f"Рука дилера после набора карт: {dealer_hand}, {total_up(dealer_hand)}")
print(f"Финальная колода: {deck}")
print()

print("Сравниваем карты между игроками")
result = compare_players_hands(player_one_hand, player_two_hand)
print(f"Рука игрока 1: {player_one_hand}, {total_up(player_one_hand)}")
print(f"Рука игрока 2: {player_two_hand}, {total_up(player_two_hand)}")
print(f"Результат между игроками: {result}")
print()

result = compare_players_with_dealer_hands(dealer_hand, player_one_hand, player_two_hand, result)
print("Сравниваем игроков и дилера")
print(f"Рука дилера: {dealer_hand}, {total_up(dealer_hand)}")
print(f"Рука игрока 1: {player_one_hand}, {total_up(player_one_hand)}")
print(f"Рука игрока 2: {player_two_hand}, {total_up(player_two_hand)}")
print(f"Результат между игроками и дилером: {result}")