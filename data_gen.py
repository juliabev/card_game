import numpy as np
import os, time, random, json
from typing import Tuple


# helpers
def ensure_dir(path: str):
    '''
    
    '''
    os.makedirs(path, exist_ok=True)

# naming files
def batch_filename_raw(batch_idx: int, batch_size: int, out_dir: str) -> str:
    '''
    
    '''
    return os.path.join(out_dir, f'_rawDecks_{batch_idx}_n={batch_size}.npz')

# generating the deck
def gen_deck_arr(rng: random.Random) -> np.ndarray:
    '''
    Return a (52,) uint8 array with exactly 26 zeros and 26 ones, shuffled.
    '''

    deck = np.array([0]*26 + [1]*26, dtype=np.uint8)
    rng.shuffle(deck)
    return deck

def simulate_batch(batch_idx: int, batch_size: int, out_dir: str, seed: int = 12345) -> str:
    '''
    Generate one batch of raw decks and save as a single npz file
    shape: (batch_size, 52), dtype=uint8, key='decks'
    Returns the file path.
    '''

    ensure_dir(out_dir)
    rng = random.Random(seed + batch_idx)

    decks = np.empty((batch_size, 52), dtype=np.uint8)
    for i in range(batch_size):
        decks[i] = gen_deck_arr(rng)

    path = batch_filename_raw(batch_idx, batch_size, out_dir)
    np.savez_compressed(path, decks=decks)
    return path

# performance
def perf_probe(out_dir: str, batch_size: int = 10_000, batches: int = 2, seed: int = 12345) -> dict:
    '''
    Measure generation + write time for raw deck batches (no scoring).
    Produces one .npz per batch and summarizes sizes/timings in perf_results.json
    '''
    ensure_dir(out_dir)
    results = {'batch_idx': [], 'gen_write_time_s': [], 'file_mb': []}
    for b in range(batches):
        t0 = time.perf_counter()
        path = simulate_batch(b, batch_size, out_dir, seed=seed)
        t1 = time.perf_counter()
        size_mb = os.path.getsize(path) / (1024**2)
        results['batch_idx'].append(b)
        results['gen_write_time_s'].append(t1 - t0)
        results['file_mb'].append(size_mb)
    with open(os.path.join(out_dir, 'perf_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    return results