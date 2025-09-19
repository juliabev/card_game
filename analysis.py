import numpy as np
import random
import os

PATH_DATA = 'data'

#full_deck = [0]*26 + [1]*26
#shuffled_deck = random.shuffle(full_deck)


player1 = ['','' ,'']

def getp1combo() -> list:
    '''
    Gives a random player 1 combo in the form of a list
    '''
    for index in range(len(player1)):
        player1[index] = random.choice(('R','B'))
    return player1

def getp2combo(list) -> list: # type hinting
    """
    Return a list of 3 choices that gives the best probability of winning the 
    humble nishiyama randomness game
    """ # docstring
    a, b, c = player1  # unpack
    flip = {"R": "B", "B": "R"}  # mapping to "not"
    return [flip[b], a, b]

def shuffle(full_deck: list) -> list:
    '''
    Shuffle deck.
    '''
    shuffled_deck = full_deck.copy()
    random.shuffle(shuffled_deck)
    return shuffled_deck

def generate_deck_files(full_deck: list, num_files = 1, decks_per_file = 1):
    '''
    Generate shuffled decks of 'R' and 'B' and saves them as 200 .npy files
    Each file contains an array of shape (decks_per_file, 52) with dtype str
    '''
    for file_idx in range(num_files):
        arr = np.empty((decks_per_file, 52), dtype=str)

        for i in range(decks_per_file):
            arr[i] = shuffle(full_deck)
        
        # save file
        filename = f'_scoredDecks_{num_files}_n={decks_per_file}.npy'
        np.save(filename, arr)
        print(f'Saved {filename} with shape {arr.shape}')


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
        print(set_of_three, "vs p1:", p1, "vs p2:", p2)


        if set_of_three == p1:
            print(f"--> MATCH for P1 at window {i}, count={count}")
            p1_tricks += 1
            p1_points += count
            count = 0
            #print(f'you have a match p1')
            
        elif set_of_three == p2:
            print(f"--> MATCH for P2 at window {i}, count={count}")
            p2_tricks += 1
            p2_points += count
            count = 0
            #print(f'you have a match p2')
    print(f" [DEBUG] Final scores: p1_tricks={p1_tricks}, p2_tricks={p2_tricks}, p1_points={p1_points}, p2_points={p2_points}")

    return p1_tricks, p2_tricks, p1_points, p2_points

def run_cardgame_on_files(num_files=1, decks_per_file = 1, p1_options = None, p2_options = None):
    '''
    Loops over the deck files, runs cardgame function on each deck, and
    saves results. Each result file will be a NumPy array of shape
    (decks_per_file, 8, 8, 2)
    '''
    for file_idx in range(num_files): # going through each file
        deck_file = f'_scoredDecks_{num_files}_n={decks_per_file}.npy'
        decks = np.load(deck_file)

        results = np.zeros((decks_per_file, len(p1_options), len(p2_options), 4), dtype=int)

        for deck_idx, deck in enumerate(decks): # going through each deck
            #print(deck)
            for p1_idx, p1_combo in enumerate(p1_options):
                for p2_idx, p2_combo in enumerate(p2_options):
                    if p1_combo == p2_combo:
                        continue # skips the identical combos
                        #print(p1_combo, p2_combo)
                    p1_tricks, p2_tricks, p1_points, p2_points = cardgame(deck.tolist(), p1_combo, p2_combo)
                        
                    results[deck_idx, p1_idx, p2_idx] = [p1_tricks, p2_tricks, p1_points, p2_points]
        
        out_file = f'_results_{file_idx}.npy'
        np.save(out_file, results)
        print(f'Processed {deck_file} -> Saved {out_file} with shape {results.shape}')
    return results



