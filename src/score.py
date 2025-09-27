import csv
import os
import itertools
from typing import Tuple

SEQUENCES = ['000', '001', '010', '011', '100', '101', '110', '111']

def score_deck(deck: str, seq1: str, seq2: str)) -> Tuple[int, int, int, int]:
    p1_cards = 0
    p2_cards = 0
    pile = 2  # first check is at 3

    p1_tricks = 0
    p2_tricks = 0

    i = 0
    n = len(deck)
    while i < n - 2:
        pile += 1
        window = deck[i:i+3]
        if window == seq1:
            p1_cards += pile
            pile = 2
            p1_tricks += 1
            i += 3
        elif window == seq2:
            p2_cards += pile
            pile = 2
            p2_tricks += 1
            i += 3
        else:
            i += 1
    return p1_cards, p2_cards, p1_tricks, p2_tricks

def calculate_winner() -> Tuple[int, int, int]:
    pass