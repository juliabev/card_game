import numpy as np
import os
import itertools
import pandas as pd
from multiprocessing import Pool, cpu_count

def get_players():
    '''Return all 8 players as 3-bit binary strings.'''
    return [f'{i:03b}' for i in range(8)]

def score_deck(deck, p1_seq, p2_seq):
    '''
    Scores a single deck for a pair of players using non-overlapping matches.
    Returns (card_winner, trick_winner), each can be 0 (draw), 1 (p1 wins), 2 (p2 wins)
    '''
    seq_len = 3
    p1_cards = 0
    p2_cards = 0
    p1_tricks = 0
    p2_tricks = 0
    pos = 0
    deck_len = len(deck)
    
    while pos <= deck_len - seq_len:
        window = deck[pos:pos+seq_len]
        if np.array_equal(window, p1_seq):
            p1_tricks += 1
            p1_cards += seq_len
            pos += seq_len  # skip matched cards
        elif np.array_equal(window, p2_seq):
            p2_tricks += 1
            p2_cards += seq_len
            pos += seq_len
        else:
            pos += 1

    # determine winners for this deck
    if p1_cards > p2_cards:
        card_winner = 1
    elif p2_cards > p1_cards:
        card_winner = 2
    else:
        card_winner = 0  # draw

    if p1_tricks > p2_tricks:
        trick_winner = 1
    elif p2_tricks > p1_tricks:
        trick_winner = 2
    else:
        trick_winner = 0  # draw

    return card_winner, trick_winner

def process_file_head_to_head(filepath):
    '''Process a single .npz file of decks.'''
    players = get_players()
    player_sequences = {p: np.array([int(c) for c in p]) for p in players}
    player_combinations = list(itertools.permutations(players, 2))
    
    data = np.load(filepath)
    decks = data['decks']
    
    results = {f'{p1}_vs_{p2}': {'p1_card_wins': 0, 'p2_card_wins': 0, 'card_draws': 0,
                                 'p1_trick_wins': 0, 'p2_trick_wins': 0, 'trick_draws': 0}
               for p1, p2 in player_combinations}

    for deck in decks:
        for p1, p2 in player_combinations:
            combo_key = f'{p1}_vs_{p2}'
            p1_seq = player_sequences[p1]
            p2_seq = player_sequences[p2]

            # skip identical sequences
            if np.array_equal(p1_seq, p2_seq):
                results[combo_key]['card_draws'] += 1
                results[combo_key]['trick_draws'] += 1
                continue

            card_winner, trick_winner = score_deck(deck, p1_seq, p2_seq)

            if card_winner == 1:
                results[combo_key]['p1_card_wins'] += 1
            elif card_winner == 2:
                results[combo_key]['p2_card_wins'] += 1
            else:
                results[combo_key]['card_draws'] += 1

            if trick_winner == 1:
                results[combo_key]['p1_trick_wins'] += 1
            elif trick_winner == 2:
                results[combo_key]['p2_trick_wins'] += 1
            else:
                results[combo_key]['trick_draws'] += 1

    return results

def run_simulation(raw_data_dir, output_csv_path, max_files=None):
    '''Run the head-to-head simulation over multiple files using multiprocessing.'''
    file_list = [os.path.join(raw_data_dir, f) for f in os.listdir(raw_data_dir) if f.endswith('.npz')]
    if max_files:
        file_list = file_list[:max_files]

    if not file_list:
        print(f'No .npz files found in {raw_data_dir}')
        return

    num_processes = cpu_count()
    print(f'Using {num_processes} processes for {len(file_list)} files.')

    final_results = {f'{p1}_vs_{p2}': {'p1_card_wins': 0, 'p2_card_wins': 0, 'card_draws': 0,
                                       'p1_trick_wins': 0, 'p2_trick_wins': 0, 'trick_draws': 0}
                     for p1, p2 in itertools.permutations(get_players(), 2)}

    with Pool(processes=num_processes) as pool:
        for i, file_results in enumerate(pool.imap_unordered(process_file_head_to_head, file_list)):
            for combo, scores in file_results.items():
                for key in scores:
                    final_results[combo][key] += scores[key]
            print(f'Processed file {i+1}/{len(file_list)}')

    # Save results to CSV
    output_data = []
    for combo, scores in final_results.items():
        p1, p2 = combo.split('_vs_')
        output_data.append({
            'player1': p1,
            'player2': p2,
            **scores
        })

    df = pd.DataFrame(output_data)
    df.to_csv(output_csv_path, index=False)
    print(f'Results saved to {output_csv_path}')