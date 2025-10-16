import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import argparse
from typing import Optional, List

SEQUENCES: List[str] = ['000','001','010','011','100','101','110','111']

def ensure_dir(path: str):
    '''
    Verify that path exists
    '''
    if path:
        os.makedirs(path, exist_ok=True)

def load_summary(path: str) -> dict:
    '''
    Loads summary from summary.json
    '''
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def _to_8x8(a) -> np.ndarray:
    '''
    
    '''
    arr = np.array(a)
    if arr.size == 64 and arr.ndim == 1:
        arr = arr.reshape(8, 8)
    if arr.shape != (8, 8):
        raise ValueError(f'Expected (8,8), got {arr.shape}')
    return arr.astype(float)

def _reindex_for_display(mat: np.ndarray) -> pd.DataFrame:
    '''
    
    '''
    # Put '000' at bottom-left by reversing row order
    df = pd.DataFrame(mat, index=SEQUENCES, columns=SEQUENCES)
    return df.loc[SEQUENCES[::-1], :]

def _pick_key(d: dict, prefer: str, fallback: str) -> str:
    if prefer in d: return prefer
    if fallback in d: return fallback
    raise KeyError(f"Neither '{prefer}' nor '{fallback}' found in summary.json")

def make_annotations(win_df: pd.DataFrame,
                     tie_df: Optional[pd.DataFrame],
                     n: Optional[int] = None) -> np.ndarray:
    win = np.rint(win_df.to_numpy() * 100).astype(int)
    ann = np.empty(win.shape, dtype=object)
    if tie_df is None:
        for i in range(win.shape[0]):
            for j in range(win.shape[1]):
                ann[i, j] = f"{win[i, j]}"
        return ann

    tie_vals = tie_df.to_numpy()
    # If we don’t know n, show tie; else show tie counts
    if n is None:
        tie_disp = (np.rint(tie_vals * 100).astype(int)).astype(str)
    else:
        tie_disp = np.rint(tie_vals * n).astype(int).astype(str)

    for i in range(win.shape[0]):
        for j in range(win.shape[1]):
            ann[i, j] = f"{win[i, j]} ({tie_disp[i, j]})"
    return ann

def plot_heatmap(win_df: pd.DataFrame,
                 ann: np.ndarray,
                 title: str,
                 out_png: str,
                 cmap: str = 'viridis') -> None:
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
    ax.set_title(title, pad=14, fontsize=14, weight='bold')
    ax.set_xlabel('P2 (me): chosen sequence', labelpad=10)
    ax.set_ylabel('P1 (opponent): chosen sequence', labelpad=10)

    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))

    plt.tight_layout()
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--summary', default=os.path.join('data', 'summary.json'),
                    help='Path to summary.json (default: data/summary.json)')
    ap.add_argument('--outdir', default='figures', help='Output directory for PNGs')
    args = ap.parse_args()

    results = load_summary(args.summary)
    n = results.get('n', None)

    # key in your code are singular: 'card_ties'/'trick_ties'
    cards_key = 'cards'
    tricks_key = 'tricks'
    cards_ties_key = _pick_key(results, 'cards_ties', 'card_ties')
    tricks_ties_key = _pick_key(results, 'tricks_ties', 'trick_ties')

    # load matrices
    cards = _reindex_for_display(_to_8x8(results[cards_key]))
    tricks = _reindex_for_display(_to_8x8(results[tricks_key]))
    cards_ties = _reindex_for_display(_to_8x8(results[cards_ties_key]))
    tricks_ties = _reindex_for_display(_to_8x8(results[tricks_ties_key]))

    # add annotations to head map
    ann_cards = make_annotations(cards, cards_ties, n=n)
    ann_tricks = make_annotations(tricks, tricks_ties, n=n)

    # Plots
    plot_heatmap(cards, ann_cards,
                 title='Chance of Winning (By Cards)',
                 out_png=os.path.join(args.outdir, 'heatmap_by_cards.png'))

    plot_heatmap(tricks, ann_tricks,
                 title='Chance of Winning (By Tricks)',
                 out_png=os.path.join(args.outdir, 'heatmap_by_tricks.png'))