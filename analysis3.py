import random
import csv
import os
import itertools
from typing import Tuple

# Sequences using 'R' and 'B'
SEQUENCES = [''.join(p) for p in itertools.product(['R', 'B'], repeat=3)]


def score_deck(deck: str, seq1: str, seq2: str) -> Tuple[int, int, int, int]:
    """
    Greedy trick-taking and 'pile' cards scoring on a single 52-char deck string ('R'/'B').
    Returns: p1_cards, p2_cards, p1_tricks, p2_tricks
    """
    p1_cards = 0
    p2_cards = 0
    pile = 2

    p1_tricks = 0
    p2_tricks = 0

    i = 0
    n = len(deck)
    while i < n - 2:
        pile += 1
        window = deck[i:i + 3]
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


def calculate_winner(
    p1_cards: int, p2_cards: int, p1_tricks: int, p2_tricks: int
) -> Tuple[int, int, int, int]:
    """
    Calculates winning player.
    Returns (cards_winner, cards_draw, tricks_winner, tricks_draw)
    where winners are 0 (P1) or 1 (P2), draws are {0,1}.
    """
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


def gen_deck_str(rng: random.Random) -> str:
    """
    26 red + 26 black; shuffled without replacement; return as 'R'/'B' string
    """
    deck = ['R'] * 26 + ['B'] * 26
    rng.shuffle(deck)
    return ''.join(deck)


def score_all_matchups_for_deck(deck: str) -> dict:
    """
    Builds a dictionary of results for this deck.
    Keys are ('seq1', 'seq2'), values are winner/tie info.
    """
    results = {}
    for s1 in SEQUENCES:
        for s2 in SEQUENCES:
            if s1 == s2:
                continue
            
            p1c, p2c, p1t, p2t = score_deck(deck, s1, s2)
            cw, cd, tw, td = calculate_winner(p1c, p2c, p1t, p2t)

            # Store results as P2 wins (+1), P1 wins (-1), or tie (0)
            cards_result = 1 if cd == 0 and cw == 1 else (-1 if cd == 0 and cw == 0 else 0)
            tricks_result = 1 if td == 0 and tw == 1 else (-1 if td == 0 and tw == 0 else 0)
            
            results[(s1, s2)] = {
                'cards': cards_result,
                'tricks': tricks_result,
            }
    return results


def ensure_dir(path: str):
    """
    Checks that directory for raw data file exists.
    """
    os.makedirs(path, exist_ok=True)


def batch_filename(batch_idx: int, batch_size: int, out_dir: str) -> str:
    """
    Creates filenames based on naming convention
    """
    return os.path.join(out_dir, f'_scoredDecks_{batch_idx}_n={batch_size}.csv')


def simulate_batch(batch_idx: int, batch_size: int, out_dir: str, seed: int = 12345) -> str:
    """
    Simulate one batch of decks; save results to .csv; return filepath.
    """
    ensure_dir(out_dir)
    rng = random.Random(seed + batch_idx)

    path = batch_filename(batch_idx, batch_size, out_dir)
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(
            ['Deck_ID', 'P1_Seq', 'P2_Seq', 'Cards_Result', 'Tricks_Result']
        )
        for i in range(batch_size):
            deck = gen_deck_str(rng)
            results = score_all_matchups_for_deck(deck)
            for (s1, s2), res in results.items():
                writer.writerow(
                    [i, s1, s2, res['cards'], res['tricks']]
                )
    return path


def summarize(out_dir: str):
    """
    Read all _scoredDecks_*.csv files; produce summary.csv with 8x8 probabilities.
    """
    cards_p2_wins = {
        (s1, s2): 0 for s1 in SEQUENCES for s2 in SEQUENCES if s1 != s2
    }
    cards_ties = {
        (s1, s2): 0 for s1 in SEQUENCES for s2 in SEQUENCES if s1 != s2
    }
    tricks_p2_wins = {
        (s1, s2): 0 for s1 in SEQUENCES for s2 in SEQUENCES if s1 != s2
    }
    tricks_ties = {
        (s1, s2): 0 for s1 in SEQUENCES for s2 in SEQUENCES if s1 != s2
    }
    
    total_games_per_matchup = 0

    for fname in sorted(os.listdir(out_dir)):
        if not (fname.startswith('_scoredDecks_') and fname.endswith('.csv')):
            continue
        
        with open(os.path.join(out_dir, fname), 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader) # Skip header row
            for row in reader:
                deck_id, p1_seq, p2_seq, cards_res, tricks_res = row
                
                cards_res = int(cards_res)
                tricks_res = int(tricks_res)
                
                matchup = (p1_seq, p2_seq)
                
                if cards_res == 1:
                    cards_p2_wins[matchup] += 1
                elif cards_res == 0:
                    cards_ties[matchup] += 1
                
                if tricks_res == 1:
                    tricks_p2_wins[matchup] += 1
                elif tricks_res == 0:
                    tricks_ties[matchup] += 1
                
                total_games_per_matchup += 1 # This will be inaccurate if matchups are not on every row

    total_games = int(total_games_per_matchup / (len(SEQUENCES) * (len(SEQUENCES)-1)))

    # Write summary to a single CSV file
    summary_path = os.path.join(out_dir, 'summary.csv')
    with open(summary_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'P1_Sequence', 'P2_Sequence', 'Total_Games', 
            'Cards_P2_Win_Prob', 'Cards_Tie_Prob', 
            'Tricks_P2_Win_Prob', 'Tricks_Tie_Prob'
        ])
        
        for s1 in SEQUENCES:
            for s2 in SEQUENCES:
                if s1 == s2:
                    continue
                
                matchup = (s1, s2)
                if total_games > 0:
                    cards_p2_win_prob = cards_p2_wins[matchup] / total_games
                    cards_tie_prob = cards_ties[matchup] / total_games
                    tricks_p2_win_prob = tricks_p2_wins[matchup] / total_games
                    tricks_tie_prob = tricks_ties[matchup] / total_games
                else:
                    cards_p2_win_prob = cards_tie_prob = tricks_p2_win_prob = tricks_tie_prob = 0.0

                writer.writerow([
                    s1, s2, total_games, 
                    f'{cards_p2_win_prob:.6f}', 
                    f'{cards_tie_prob:.6f}', 
                    f'{tricks_p2_win_prob:.6f}', 
                    f'{tricks_tie_prob:.6f}'
                ])
    print(f"Summary written to {summary_path}")