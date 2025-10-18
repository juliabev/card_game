import numpy as np
import os
import itertools
import pandas as pd
from multiprocessing import Pool, cpu_count


def get_players():
    '''
    Returns the len 8 sequences of players possible ['000', ... , '111']
    '''
    return [f'{i:03b}' for i in range(8)]


def deck_to_windows(deck_bits: np.ndarray) -> np.ndarray:
    '''
    Convert a (52,) uint8 0/1 deck into (50,) uint8 window codes 0..7
    where each code is the 3-bit integer at positions [i, i+1, i+2].
    '''
    a = deck_bits
    # (a[i] << 2) | (a[i+1] << 1) | a[i+2]
    return (a[:-2] << 2) | (a[1:-1] << 1) | a[2:]

def score_pair_on_windows(win: np.ndarray, s1_code: int, s2_code: int) -> tuple[int, int, int, int]:
    '''
    Head to head, greedy scoring for one combination of scores (player1 vs player) 
    which is performed on a single deck:

    Returns: (p1_cards, p2_cards, p1_tricks, p2_tricks)
    '''
    pile = 2 # starts at index 2 (3)
    i = 0
    n = len(win)  # 50
    p1c = p2c = p1t = p2t = 0

    while i < n:
        pile += 1
        w = win[i]
        if w == s1_code:
            p1c += pile
            p1t += 1
            pile = 2
            i += 3
        elif w == s2_code:
            p2c += pile
            p2t += 1
            pile = 2
            i += 3
        else:
            i += 1

    return p1c, p2c, p1t, p2t

# processing files
def process_file_optimized(filepath: str) -> tuple[dict, int]:
    '''
    Processes a single .npz 'decks' file with true head-to-head scoring utilizing
    functions above.
    
    Aggregates totals and outcome counts (wins/ties by cards and by tricks)
    for all ordered pairs (with the exception of any diagonal pairs of comb;
    i.e. 000 vs 000). 
    
    Returns (results_dict, num_decks_in_file).
    '''
    players = get_players()
    seq_codes = [int(p, 2) for p in players]  # 0..7

    data = np.load(filepath)
    decks = data['decks']  # shape (N, 52), uint8
    num_decks_in_file = len(decks)

    if num_decks_in_file == 0:
        return {}, 0

    # Initialize aggregation container per pair
    results = {
        f'{players[i]}_vs_{players[j]}': {
            'p1_total_cards': 0, 'p2_total_cards': 0,
            'p1_total_tricks': 0, 'p2_total_tricks': 0,
            'cards_p1_wins': 0, 'cards_p2_wins': 0, 'cards_ties': 0,
            'tricks_p1_wins': 0, 'tricks_p2_wins': 0, 'tricks_ties': 0,
        }
        for i, j in itertools.permutations(range(8), 2)
    }

    # processes each deck once; reuses its window for all pairs
    for d in range(num_decks_in_file):
        win = deck_to_windows(decks[d])

        for i, j in itertools.permutations(range(8), 2):
            key = f'{players[i]}_vs_{players[j]}'
            p1c, p2c, p1t, p2t = score_pair_on_windows(win, seq_codes[i], seq_codes[j])

            # totals
            r = results[key]
            r['p1_total_cards']  += p1c
            r['p2_total_cards']  += p2c
            r['p1_total_tricks'] += p1t
            r['p2_total_tricks'] += p2t

            # Outcomes: cards
            if p1c > p2c:
                r['cards_p1_wins'] += 1
            elif p2c > p1c:
                r['cards_p2_wins'] += 1
            else:
                r['cards_ties'] += 1

            # Outcomes: tricks
            if p1t > p2t:
                r['tricks_p1_wins'] += 1
            elif p2t > p1t:
                r['tricks_p2_wins'] += 1
            else:
                r['tricks_ties'] += 1

    return results, num_decks_in_file


def run_simulation(raw_data_dir: str, output_csv_path: str):
    '''
    Parallel over .npz files, aggregate head-to-head totals and outcome counts,
    and save one CSV with totals and per-deck averages.
    '''
    file_list = [os.path.join(raw_data_dir, f) for f in os.listdir(raw_data_dir) if f.endswith('.npz')]

    if not file_list:
        print(f'No .npz files found in {raw_data_dir}. Please generate the data first.')
        return

    num_processes = cpu_count()
    print(f'Using {num_processes} processes for parallel execution.')

    with Pool(processes=num_processes) as pool:
        processed_results = pool.map(process_file_optimized, file_list)

    total_decks = 0
    # initialize dict (aggregator)
    final_results = {
        f'{p1}_vs_{p2}': {
            'p1_total_cards': 0, 'p2_total_cards': 0,
            'p1_total_tricks': 0, 'p2_total_tricks': 0,
            'cards_p1_wins': 0, 'cards_p2_wins': 0, 'cards_ties': 0,
            'tricks_p1_wins': 0, 'tricks_p2_wins': 0, 'tricks_ties': 0,
        }
        for p1, p2 in itertools.permutations(get_players(), 2)
    }

    # reducing results of files through aggregation
    for single_file_results, n_in_file in processed_results:
        total_decks += n_in_file
        if not single_file_results:
            continue
        for combo, scores in single_file_results.items():
            agg = final_results[combo]
            for k, v in scores.items():
                agg[k] += v

    # building rows of csv files
    rows = []
    for combo, s in final_results.items():
        p1, p2 = combo.split('_vs_')
        # calculating probabilities (avgs) for results of combs
        denom = max(total_decks, 1)
        rows.append({
            'player1': p1, 'player2': p2,
            'p1_cards': s['p1_total_cards'],  'p2_cards': s['p2_total_cards'],
            'p1_tricks': s['p1_total_tricks'],'p2_tricks': s['p2_total_tricks'],

            'cards_p1_wins': s['cards_p1_wins'],
            'cards_p2_wins': s['cards_p2_wins'],
            'cards_ties': s['cards_ties'],

            'tricks_p1_wins': s['tricks_p1_wins'],
            'tricks_p2_wins': s['tricks_p2_wins'],
            'tricks_ties': s['tricks_ties'],

            # Optional rates (per deck)
            'cards_p1_win_rate': s['cards_p1_wins'] / denom,
            'cards_p2_win_rate': s['cards_p2_wins'] / denom,
            'cards_tie_rate':    s['cards_ties']    / denom,

            'tricks_p1_win_rate': s['tricks_p1_wins'] / denom,
            'tricks_p2_win_rate': s['tricks_p2_wins'] / denom,
            'tricks_tie_rate':    s['tricks_ties']    / denom,
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv_path, index=False)
    print(f'Results saved to {output_csv_path}\nTotal decks processed: {total_decks}')
    return total_decks


