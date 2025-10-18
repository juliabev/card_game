import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

from typing import List

SEQUENCES_BINARY: List[str] = ['000','001','010','011','100','101','110','111']
SEQUENCES_MAPPED: List[str] = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
SEQUENCE_MAP = dict(zip(SEQUENCES_BINARY, SEQUENCES_MAPPED))


def ensure_dir(path: str):
    '''
    Verify that path exists
    '''
    if path:
        os.makedirs(path, exist_ok=True)



def make_annotations(win_df: pd.DataFrame, tie_rate_df: pd.DataFrame) -> np.ndarray:
    '''
    Creates annotation strings showing win % and tie %.
    '''
    win_np = win_df.to_numpy()
    tie_rate_np = tie_rate_df.to_numpy()
    ann = np.empty(win_np.shape, dtype=object)

    for i in range(win_np.shape[0]):
        for j in range(win_np.shape[1]):
            if np.isnan(win_np[i, j]):
                ann[i, j] = ''
            else:
                win_val = int(np.rint(win_np[i, j] * 100))
                tie_val = int(np.rint(tie_rate_np[i, j] * 100))
                ann[i, j] = f'{win_val} ({tie_val})'
    return ann

def plot_heatmap(win_df: pd.DataFrame,
                 ann: np.ndarray,
                 title: str,
                 out_png: str,
                 total_decks: int,
                 cmap: str = 'Blues') -> None:
    '''
    Generates and saves a styled heatmap plot.
    '''
    ensure_dir(os.path.dirname(out_png))
    plt.figure(figsize=(9, 8))
    ax = sns.heatmap(
        win_df,
        vmin=0, vmax=1,
        cmap=cmap,
        square=True,
        linewidths=0.5,
        linecolor='white',
        cbar_kws={'shrink': 0.9},
        annot=ann,
        fmt='',
        annot_kws={'fontsize': 9}
    )
    ax.set_title(f'{title} - {total_decks} Decks Simulated', pad=14, fontsize=14, weight='bold')

    plt.tight_layout()
    plt.savefig(out_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[viz] Saved heatmap to {os.path.abspath(out_png)}")

def run_visualization(csv_path: str, outdir: str, total_decks: int):
    '''
    Main function to read scoring CSV and generate heatmap visualizations.
    '''
    if not os.path.exists(csv_path):
        print(f'Error: CSV file not found at {csv_path}')
        return

    df = pd.read_csv(csv_path, dtype={'player1': str, 'player2': str})

    # Initialize 8x8 matrices for win and tie rates
    cards_wins = pd.DataFrame(np.nan, index=SEQUENCES_BINARY, columns=SEQUENCES_BINARY)
    tricks_wins = pd.DataFrame(np.nan, index=SEQUENCES_BINARY, columns=SEQUENCES_BINARY)
    cards_ties = pd.DataFrame(np.nan, index=SEQUENCES_BINARY, columns=SEQUENCES_BINARY)
    tricks_ties = pd.DataFrame(np.nan, index=SEQUENCES_BINARY, columns=SEQUENCES_BINARY)

    # Populate matrices from the CSV data
    for _, row in df.iterrows():
        p1 = row['player1']
        p2 = row['player2']
        cards_wins.loc[p1, p2] = row['cards_p2_win_rate']
        tricks_wins.loc[p1, p2] = row['tricks_p2_win_rate']
        cards_ties.loc[p1, p2] = row['cards_tie_rate']
        tricks_ties.loc[p1, p2] = row['tricks_tie_rate']

    cards_wins.rename(index=SEQUENCE_MAP, columns=SEQUENCE_MAP, inplace=True)
    tricks_wins.rename(index=SEQUENCE_MAP, columns=SEQUENCE_MAP, inplace=True)
    cards_ties.rename(index=SEQUENCE_MAP, columns=SEQUENCE_MAP, inplace=True)
    tricks_ties.rename(index=SEQUENCE_MAP, columns=SEQUENCE_MAP, inplace=True)

    # Reorder rows for display
    cards_wins_disp = cards_wins
    tricks_wins_disp = tricks_wins
    cards_ties_disp = cards_ties
    tricks_ties_disp = tricks_ties

    # Create annotation labels
    ann_cards = make_annotations(cards_wins_disp, cards_ties_disp)
    ann_tricks = make_annotations(tricks_wins_disp, tricks_ties_disp)

    # Generate and save plots
    plot_heatmap(cards_wins_disp, ann_cards,
                 title='My Chance of Winning(Draw) by Cards',
                 out_png=os.path.join(outdir, 'heatmap_by_cards.png'),
                 total_decks=total_decks)

    plot_heatmap(tricks_wins_disp, ann_tricks,
                 title='My Chance of Winning(Draw) by Tricks',
                 out_png=os.path.join(outdir, 'heatmap_by_tricks.png'),
                 total_decks=total_decks)
