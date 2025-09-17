import numpy as np
import os, time, math, random, json
from typing import Tuple

SEQUENCES = ['000','001','010','011','100','101','110','111']  # p1 rows, p2 cols
'''
'''

def score_deck(deck: str, seq1: str, seq2: str) -> Tuple[int,int,int,int]:
    ''' 
    Greedy trick-taking and 'pile' cards scoring on a single 52-char deck string ('0'/'1').
    Returns: p1_cards, p2_cards, p1_tricks, p2_tricks
    '''
    p1_cards = 0
    p2_cards = 0
    pile = 2  # first check at 3

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

def calculate_winner(p1_cards: int, p2_cards: int, p1_tricks: int, p2_tricks: int) -> Tuple[int,int,int,int]:
    '''
    Calculates winning player.
    Returns (cards_winner, cards_draw, tricks_winner, tricks_draw) where winners are 0 (P1) or 1 (P2), draws are {0,1}.
    '''
    cards_winner = 0
    cards_draw = 0
    tricks_winner = 0
    tricks_draw = 0

    if p1_cards < p2_cards:
        cards_winner = 1
    elif p1_cards == p2_cards:
        cards_draw = 1

    if p1_tricks < p2_tricks:
        tricks_winner = 1
    elif p1_tricks == p2_tricks:
        tricks_draw = 1

    return cards_winner, cards_draw, tricks_winner, tricks_draw

# functions below are to aid in simulations

def gen_deck_str(rng: random.Random) -> str:
    '''
    26 zeros + 26 ones; shuffled without replacement; return as '0/1' string
    '''
    deck = ['0'] * 26 + ['1'] * 26
    rng.shuffle(deck)
    return ''.join(deck)

def score_all_matchups_for_deck(deck: str) -> np.ndarray:
    '''
    Build a (2, 8, 8) int 8 matrix of results for this deck:
    metric 0 = cards, metric 1 = tricks; cell in {-1, 0, +1}.
    '''
    cards = np.zeros((8,8), dtype=np.int8)
    tricks = np.zeros((8,8), dtype=np.int8)

    for r, s1 in enumerate(SEQUENCES):        # p1 = row
        for c, s2 in enumerate(SEQUENCES):    # p2 = col
            p1c, p2c, p1t, p2t = score_deck(deck, s1, s2)
            cw, cd, tw, td = calculate_winner(p1c, p2c, p1t, p2t)

            # convert to signed result: +1=P2 win, -1=P1 win, 0=tie
            cards[r, c]  =  1 if cd == 0 and cw == 1 else (-1 if cd == 0 and cw == 0 else 0)
            tricks[r, c] =  1 if td == 0 and tw == 1 else (-1 if td == 0 and tw == 0 else 0)

    out = np.zeros((2,8,8), dtype=np.int8)
    out[0] = cards
    out[1] = tricks
    return out


def ensure_dir(path: str):
    '''
    Checks that directory for raw data file exists.
    '''
    os.makedirs(path, exist_ok=True)

def batch_filename(batch_idx: int, batch_size: int, out_dir: str) -> str:
    '''
    Creates filenames based on naming convention
    '''
    return os.path.join(out_dir, f'_scoredDecks_{batch_idx}_n={batch_size}.npy')

def simulate_batch(batch_idx: int, batch_size: int, out_dir: str, seed: int = 12345) -> str:
    '''
    Simulate one batch of decks; save (batch, 2, 8, 8) int8 to .npy; return filepath.
    '''
    ensure_dir(out_dir)
    rng = random.Random(seed + batch_idx)

    res = np.empty((batch_size, 2, 8, 8), dtype=np.int8)
    for i in range(batch_size):
        deck = gen_deck_str(rng)
        res[i] = score_all_matchups_for_deck(deck)

    path = batch_filename(batch_idx, batch_size, out_dir)
    np.save(path, res)
    return path

def summarize(out_dir: str) -> str:
    '''
    Read all _scoredDecks_*.npy files; produce summary.json with 8x8 probabilities.
    '''
    # tallies
    cards_p2   = np.zeros((8,8), dtype=np.int64)
    cards_ties = np.zeros((8,8), dtype=np.int64)
    cards_tot  = np.zeros((8,8), dtype=np.int64)

    tricks_p2   = np.zeros((8,8), dtype=np.int64)
    tricks_ties = np.zeros((8,8), dtype=np.int64)
    tricks_tot  = np.zeros((8,8), dtype=np.int64)

    for fname in sorted(os.listdir(out_dir)):
        if not (fname.startswith('_scoredDecks_') and fname.endswith('.npy;')):
            continue
        arr = np.load(os.path.join(out_dir, fname))  # (n,2,8,8)
        cards_res  = arr[:, 0, :, :]  # -1/0/+1
        tricks_res = arr[:, 1, :, :]

        cards_p2   += (cards_res  ==  1).sum(axis=0)
        cards_ties += (cards_res  ==  0).sum(axis=0)
        cards_tot  += cards_res.shape[0]

        tricks_p2   += (tricks_res ==  1).sum(axis=0)
        tricks_ties += (tricks_res ==  0).sum(axis=0)
        tricks_tot  += tricks_res.shape[0]

    def safe_div(a, b):
        out = np.divide(a, b, where=(b!=0), dtype=float)
        out[b==0] = 0.0
        return out

    summary = {
        'cards':       safe_div(cards_p2,   cards_tot).tolist(),
        'tricks':      safe_div(tricks_p2,  tricks_tot).tolist(),
        'card_ties':   safe_div(cards_ties, cards_tot).tolist(),
        'trick_ties':  safe_div(tricks_ties,tricks_tot).tolist(),
    }

    with open(os.path.join(out_dir, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    return os.path.join(out_dir, 'summary.json')

# quantitative test

def perf_probe(out_dir: str, batch_size: int = 10_000, batches: int = 2) -> dict:
    ensure_dir(out_dir)
    results = {'batch_idx': [], 'gen_score_time_s': [], 'write_time_s': [], 'file_mb': []}
    for b in range(batches):
        t0 = time.perf_counter()
        path = simulate_batch(b, batch_size, out_dir)
        t1 = time.perf_counter()
        size_mb = os.path.getsize(path) / (1024**2)
        t2 = time.perf_counter()
        results['batch_idx'].append(b)
        results['gen_score_time_s'].append(t1 - t0)
        results['write_time_s'].append(t2 - t1)
        results['file_mb'].append(size_mb)
    with open(os.path.join(out_dir, 'perf_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    return results
