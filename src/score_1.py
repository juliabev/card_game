import numpy as np
import os
import itertools
import pandas as pd
from multiprocessing import Pool, cpu_count
from numpy.lib.stride_tricks import sliding_window_view

def get_players():
    '''
    Returns a list of all 8 players, represented as 3-bit binary strings.
    '''
    return [f'{i:03b}' for i in range(8)]

def process_file_head_to_head_vectorized(filepath: str) -> dict:
    """
    Processes a single data file for head-to-head matchups using vectorized operations.
    """

def play_game_ju_optimized_v2(decks: np.ndarray, player_sequences: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    '''
    Scores games for all players across all decks, calculating both 'cards'
    (sum of (match_index + sequence_length) for each match) and 'tricks'
    (occurrences of player sequence).
    This version is optimized to reduce nested loops.
    '''
    num_decks, deck_size = decks.shape
    num_players = len(player_sequences)
    player_seq_len = len(player_sequences[0])

    cards_scores = np.zeros((num_decks, num_players), dtype=int)
    tricks_scores = np.zeros((num_decks, num_players), dtype=int)

    # Create a dictionary for quick lookups of player sequences
    player_map = {tuple(p_seq): i for i, p_seq in enumerate(player_sequences)}

    for deck_idx in range(num_decks):
        current_deck = decks[deck_idx]
        for i in range(deck_size - player_seq_len + 1):
            window = tuple(current_deck[i:i+player_seq_len])
            if window in player_map:
                player_idx = player_map[window]
                tricks_scores[deck_idx, player_idx] += 1
                cards_scores[deck_idx, player_idx] += (i + player_seq_len)

    return cards_scores, tricks_scores

def process_file_optimized(filepath: str) -> tuple[dict, int]:
    '''
    Processes a single data file and returns the aggregated scores.
    '''

    players = get_players()
    player_sequences = {p: np.array([int(c) for c in p]) for p in players}
    player_combinations = list(itertools.permutations(players, 2))
    
    data = np.load(filepath)
    decks = data['decks']
    deck_size = decks.shape[1]
    seq_len = 3
    
    results = {f'{p1}_vs_{p2}': {'p1_card_wins': 0, 'p2_card_wins': 0, 'card_draws': 0, 'p1_trick_wins': 0, 'p2_trick_wins': 0, 'trick_draws': 0} for p1, p2 in player_combinations}


    for deck in decks:
        # Step 1: Find all matches for all players in the deck using vectorization
        matches = {p: [] for p in players}
        windows = sliding_window_view(deck, window_shape=seq_len)
        for p, p_seq in player_sequences.items():
            matches[p] = np.where(np.all(windows == p_seq, axis=1))[0]

        # Step 2: Play head-to-head games using the pre-computed matches
        for p1, p2 in player_combinations:
            combo_key = f'{p1}_vs_{p2}'

            if np.array_equal(player_sequences[p1], player_sequences[p2]):
                results[combo_key]['card_draws'] += 1
                results[combo_key]['trick_draws'] += 1
                continue

            p1_matches = matches[p1]
            p2_matches = matches[p2]
            
            p1_cards, p1_tricks = 0, 0
            p2_cards, p2_tricks = 0, 0

            all_matches = sorted([(pos, 'p1') for pos in p1_matches] + [(pos, 'p2') for pos in p2_matches])

            current_pos = -1
            for pos, player in all_matches:
                if pos > current_pos:
                    if player == 'p1':
                        p1_tricks += 1
                        p1_cards += (pos + seq_len)
                    else: # player == 'p2'
                        p2_tricks += 1
                        p2_cards += (pos + seq_len)
                    current_pos = pos

            # Card wins/draws
            if p1_cards > p2_cards:
                results[combo_key]['p1_card_wins'] += 1
            elif p2_cards > p1_cards:
                results[combo_key]['p2_card_wins'] += 1
            else:
                results[combo_key]['card_draws'] += 1
                
            # Trick wins/draws
            if p1_tricks > p2_tricks:
                results[combo_key]['p1_trick_wins'] += 1
            elif p2_tricks > p1_tricks:
                results[combo_key]['p2_trick_wins'] += 1
            else:
                results[combo_key]['trick_draws'] += 1
                
    return results

def run_simulation_head_to_head(raw_data_dir: str, output_csv_path: str, max_files: int = None):
    """
    Runs the head-to-head simulation in parallel and saves the results.
    """
    file_list = [os.path.join(raw_data_dir, f) for f in os.listdir(raw_data_dir) if f.endswith(".npz")]
    if max_files:
        file_list = file_list[:max_files]

def run_simulation_ju(raw_data_dir: str, output_csv_path: str):
    '''
    Runs the simulation in parallel for all decks and all player combinations and saves the results to a CSV file.
    '''
    file_list = [os.path.join(raw_data_dir, f) for f in os.listdir(raw_data_dir) if f.endswith('.npz')]


    if not file_list:
        print(f'No .npz files found in {raw_data_dir}. Please generate the data first.')
        return

    num_files = len(file_list)
    num_processes = cpu_count()

    print(f"Using {num_processes} processes for parallel execution on {num_files} files.")

    final_results = {f'{p1}_vs_{p2}': {'p1_card_wins': 0, 'p2_card_wins': 0, 'card_draws': 0, 'p1_trick_wins': 0, 'p2_trick_wins': 0, 'trick_draws': 0} for p1, p2 in itertools.permutations(get_players(), 2)}

    print(f'Using {num_processes} processes for parallel execution.')


    with Pool(processes=num_processes) as pool:
        for i, single_file_results in enumerate(pool.imap_unordered(process_file_head_to_head_vectorized, file_list)):
            for combo, scores in single_file_results.items():
                final_results[combo]['p1_card_wins'] += scores['p1_card_wins']
                final_results[combo]['p2_card_wins'] += scores['p2_card_wins']
                final_results[combo]['card_draws'] += scores['card_draws']
                final_results[combo]['p1_trick_wins'] += scores['p1_trick_wins']
                final_results[combo]['p2_trick_wins'] += scores['p2_trick_wins']
                final_results[combo]['trick_draws'] += scores['trick_draws']
            print(f"Processed file {i+1}/{num_files}")

    output_data = []
    for combo, scores in final_results.items():
        p1, p2 = combo.split('_vs_')
        output_data.append({
            'player1': p1,
            'player2': p2,
            'p1_card_wins': scores['p1_card_wins'],
            'p2_card_wins': scores['p2_card_wins'],
            'card_draws': scores['card_draws'],
            'p1_trick_wins': scores['p1_trick_wins'],
            'p2_trick_wins': scores['p2_trick_wins'],
            'trick_draws': scores['trick_draws'],
        })

    df = pd.DataFrame(output_data)
    df.to_csv(output_csv_path, index=False)
    print(f'Results saved to {output_csv_path}')

if __name__ == '__main__':
    run_simulation_head_to_head('raw_data', 'scoring_results_head_to_head_1M.csv', max_files=100)
