import numpy as np
import random



full_deck = [0]*26 + [1]*26
shuffled_deck = random.shuffle(full_deck)


random.shuffle()

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

def cardgame(list):
    '''
    When you give a deck of 
    '''
