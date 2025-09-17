import numpy as np
import random

#full_deck = [0]*26 + [1]*26
#shuffled_deck = random.shuffle(full_deck)


player1 = [0,0,0]

def getp1combo() -> list:
    '''
    Gives a random player 1 combo in the form of a list
    '''
    for index in range(len(player1)):
        player1[index] = random.choice((0,1))
    return player1

def getp2combo(list) -> list: # type hinting
    """
    Return a list of 3 numbers that gives the best probability of winning the 
    humble nishiyama randomness game
    """ # docstring

    a, b, c = player1
    return [1 - b, a, b]

def shuffle(full_deck: list) -> list:
    '''
    Shuffle deck.
    '''
    shuffled_deck = full_deck.copy()
    random.shuffle(shuffled_deck)
    return shuffled_deck

def cardgame(deck: list, p1: list, p2: list):
    '''
    Using the deck provided, this function will give the windows of the deck
    '''
    p1_tricks = 0
    p2_tricks = 0

    p1_points = 0
    p2_points = 0

    count = 0
    for i in range(len(deck)-2):
        count += 1

        set_of_three = deck[i:i+3]
        print(i, set_of_three)

        if set_of_three == p1:
            print(f'Player 1, your choice was matched! the combination {p1} matched {set_of_three}')
            p1_tricks += 1
            p1_points += count
            count = 0
            
        elif set_of_three == p2:
            print(f'Player 2, your choice was matched! the combination {p2} matched {set_of_three}')
            p2_tricks += 1
            p2_points += count
            count = 0

    return p1_tricks, p2_tricks, p1_points, p2_points




