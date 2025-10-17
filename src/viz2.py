=======
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import os
from src.data_gen import simulate_batch
from src.score_2 import run_simulation

def get_players():
    '''
    Returns the len 8 sequences of players possible ['000', ... , '111']
    '''
    return [f'{i:03b}' for i in range(8)]

def create_heatmap(csv_path: str, scoring_method: str, output_dir: str):
    """
    Generates and saves a heatmap from scoring data, with annotations and styling.

    Args:
        csv_path (str): Path to the input CSV file with scoring results.
        scoring_method (str): The scoring method ('By Tricks' or 'By Cards') to visualize.
        output_dir (str): Directory to save the generated heatmap image.
    """
    if not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    if scoring_method == 'By Tricks':
        win_rate_col = 'tricks_p1_win_rate'
        tie_rate_col = 'tricks_tie_rate'
    elif scoring_method == 'By Cards':
        win_rate_col = 'cards_p1_win_rate'
        tie_rate_col = 'cards_tie_rate'
    else:
        print("Invalid scoring method. Choose 'By Tricks' or 'By Cards'.")
        return

    total_decks = df['cards_p1_wins'].sum() + df['cards_p2_wins'].sum() + df['cards_ties'].sum()
    
    players = get_players()
    heatmap_data = pd.DataFrame(np.zeros((len(players), len(players))), index=players, columns=players)
    prob_data = pd.DataFrame(np.zeros((len(players), len(players))), index=players, columns=players)

    for _, row in df.iterrows():
        p1 = row['player1']
        p2 = row['player2']
        win_rate = row[win_rate_col]
        tie_rate = row[tie_rate_col]
        
        heatmap_data.loc[p2, p1] = win_rate * 100
        prob_data.loc[p2, p1] = (win_rate + tie_rate) * 100

    annot_labels = np.array([f"{win:.0f}({draw:.0f})" for win, draw in zip(heatmap_data.values.flatten(), prob_data.values.flatten())]).reshape(heatmap_data.shape)
    
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(heatmap_data, annot=annot_labels, fmt="", cmap="viridis", linewidths=.5, cbar_kws={'label': 'Win Probability (%)'})
    
    for i in range(len(players)):
        max_win_prob_row = heatmap_data.iloc[i].max()
        for j in range(len(players)):
            if heatmap_data.iloc[i, j] == max_win_prob_row:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=False, edgecolor='black', lw=2))

    plt.title(f'Win Probability Matrix ({scoring_method}) - Sample Size: {total_decks}')
    plt.xlabel('My Choice')
    plt.ylabel('Opponent Choice')
    
    output_path = os.path.join(output_dir, f'heatmap_{scoring_method.replace(" ", "_").lower()}.png')
    plt.savefig(output_path)
    plt.close()
    print(f"Heatmap saved to {output_path}")

def augment_data(n: int, raw_data_dir: str = 'raw_data', results_dir: str = 'results'):
    """
    Generates n new decks, updates scores, and creates new visualizations.

    Args:
        n (int): The number of new decks to generate.
        raw_data_dir (str): Directory to store raw deck data.
        results_dir (str): Directory to store scoring results and visualizations.
    """
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Generate new decks
    batch_idx = len(os.listdir(raw_data_dir))
    simulate_batch(batch_idx, n, raw_data_dir)
    
    # Run simulation on all raw data
    output_csv_path = os.path.join(results_dir, 'scoring_results.csv')
    run_simulation(raw_data_dir, output_csv_path)
    
    # Create heatmaps
    create_heatmap(output_csv_path, 'By Tricks', results_dir)
    create_heatmap(output_csv_path, 'By Cards', results_dir)
>>>>>>> 981249fd05a17de341b916c39c909cdfd978a85e
