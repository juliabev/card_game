import numpy as np

player1 = [0,0,0]


def player2(n: int=3, low: int=0, high: int=25): # type hinting
    """
    Return a list of 3 numbers that gives the best probability of winning the 
    humble nishiyama randomness game
    """ # docstring

    return np.random.randint(low=low, high=high+1, size=(n,2))