import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Создание колоды
def make_decks(num_decks, card_types):
    new_deck = []
    for i in range(num_decks):
        for j in range(4):
            new_deck.extend(card_types)
    random.shuffle(new_deck)
    return new_deck


# Эта функция перечисляет все комбинации значений туза в
# массив sum_array.
# Например, если у вас 2 туза, есть 4 комбинации:
# [[1,1], [1,11], [11,1], [11,11]]
# Эти комбинации приводят к 3 уникальным суммам: [2, 12, 22]
# Из этих 3 только 2 являются <= 21, поэтому они возвращаются: [2, 12]+
def get_ace_values(temp_list):
    sum_array = np.zeros((2 ** len(temp_list), len(temp_list)))
    # Этот цикл получает комбинации
    for i in range(len(temp_list)):
        n = len(temp_list) - i
        half_len = int(2 ** n * 0.5)
        for rep in range(int(sum_array.shape[0] / half_len / 2)):
            sum_array[rep * 2 ** n: rep * 2 ** n + half_len, i] = 1
            sum_array[rep * 2 ** n + half_len: rep * 2 ** n + half_len * 2, i] = 11
            # Только значения, которые подходят (<=21)
    return list(set([int(s) for s in np.sum(sum_array, axis=1) \
                     if s <= 21]))  # Конвертация num_aces, int в list


# Например, если num_aces = 2, вывод должен быть [[1,11],[1,11]]
# Нужен этот формат для функции get_ace_values
def ace_values(num_aces):
    temp_list = []
    for i in range(num_aces):
        temp_list.append([1, 11])
    return get_ace_values(temp_list)


# Сумма на руках
def total_up(hand):
    aces = 0
    total = 0

    for card in hand:
        if card != 'A':
            total += card
        else:
            aces += 1

    # Вызовите функцию ace_values, чтобы получить список возможных значений для тузов на руках.
    ace_value_list = ace_values(aces)
    final_totals = [i + total for i in ace_value_list if i + total <= 21]

    if final_totals == []:
        return min(ace_value_list) + total
    else:
        return max(final_totals)

