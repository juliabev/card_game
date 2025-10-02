import numpy as np
import os
import itertools
import pandas as pd
from multiprocessing import Pool, cpu_count

def get_players():
    """
    Returns a list of all 8 players, represented as 3-bit binary strings.
    """
    return [f'{i:03b}' for i in range(8)]

def play_game_ju_optimized_v2(decks: np.ndarray, player_sequences: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """
    Scores games for all players across all decks, calculating both 'cards'
    (sum of (match_index + sequence_length) for each match) and 'tricks'
    (occurrences of player sequence).
    This version is optimized to reduce nested loops.
    """
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
    """
    Processes a single data file and returns the aggregated scores.
    """
    players = get_players()
    player_sequences = [np.array([int(c) for c in p]) for p in players]
    
    data = np.load(filepath)
    decks = data['decks']
    num_decks_in_file = len(decks)

    if num_decks_in_file == 0:
        return {}, 0

    cards_scores, tricks_scores = play_game_ju_optimized_v2(decks, player_sequences)
    
    player_combinations = list(itertools.permutations(range(len(players)), 2))
    
    results = {}
    for i, j in player_combinations:
        p1, p2 = players[i], players[j]
        p1_total_cards = np.sum(cards_scores[:, i])
        p1_total_tricks = np.sum(tricks_scores[:, i])
        p2_total_cards = np.sum(cards_scores[:, j])
        p2_total_tricks = np.sum(tricks_scores[:, j])
        
        results[f'{p1}_vs_{p2}'] = {
            'p1_total_cards': p1_total_cards,
            'p1_total_tricks': p1_total_tricks,
            'p2_total_cards': p2_total_cards,
            'p2_total_tricks': p2_total_tricks
        }
        
    return results, num_decks_in_file

def run_simulation_ju(raw_data_dir: str, output_csv_path: str):
    """
    Runs the simulation in parallel for all decks and all player combinations and saves the results to a CSV file.
    """
    file_list = [os.path.join(raw_data_dir, f) for f in os.listdir(raw_data_dir) if f.endswith(".npz")]

    if not file_list:
        print(f"No .npz files found in {raw_data_dir}. Please generate the data first.")
        return

    num_processes = cpu_count()
    print(f"Using {num_processes} processes for parallel execution.")

    with Pool(processes=num_processes) as pool:
        processed_results = pool.map(process_file_optimized, file_list)

    total_decks = 0
    final_results = {f'{p1}_vs_{p2}': {'p1_total_cards': 0, 'p1_total_tricks': 0, 'p2_total_cards': 0, 'p2_total_tricks': 0} for p1, p2 in itertools.permutations(get_players(), 2)}

    for single_file_results, num_decks_in_file in processed_results:
        total_decks += num_decks_in_file
        if not single_file_results:
            continue
        for combo, scores in single_file_results.items():
            final_results[combo]['p1_total_cards'] += scores['p1_total_cards']
            final_results[combo]['p1_total_tricks'] += scores['p1_total_tricks']
            final_results[combo]['p2_total_cards'] += scores['p2_total_cards']
            final_results[combo]['p2_total_tricks'] += scores['p2_total_tricks']

    output_data = []
    for combo, scores in final_results.items():
        p1, p2 = combo.split('_vs_')
        p1_total_cards = scores['p1_total_cards']
        p1_total_tricks = scores['p1_total_tricks']
        p2_total_cards = scores['p2_total_cards']
        p2_total_tricks = scores['p2_total_tricks']
        output_data.append({
            'player1': p1,
            'player2': p2,
            'p1_cards': p1_total_cards,
            'p1_tricks': p1_total_tricks,
            'p2_cards': p2_total_cards,
            'p2_tricks': p2_total_tricks,
            'p1_avg_cards': p1_total_cards / total_decks if total_decks > 0 else 0,
            'p1_avg_tricks': p1_total_tricks / total_decks if total_decks > 0 else 0,
            'p2_avg_cards': p2_total_cards / total_decks if total_decks > 0 else 0,
            'p2_avg_tricks': p2_total_tricks / total_decks if total_decks > 0 else 0,
        })

    df = pd.DataFrame(output_data)
    df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")

if __name__ == '__main__':
    run_simulation_ju('raw_data', 'scoring_results_ju_optimized_v2.csv')
