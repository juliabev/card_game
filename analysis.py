import numpy as np

player1 = [1,1,1]


def getp2combo(list) -> list: # type hinting
    """
    Return a list of 3 numbers that gives the best probability of winning the 
    humble nishiyama randomness game
    """ # docstring
    
    for index, j in enumerate(player1):
        player2 = [0,0,0]
        if index == 1:
            if j == 0:
               player2[0] == 1
            else:
               player2[0] == 0
        
        player2[1] == player1[0]
        player2[2] == player1[1]
    return player2
