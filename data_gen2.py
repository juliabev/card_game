import numpy as np
import os, time, random, json

def ensure_dir(path: str):
    '''
    Ensure output directory exists.
    '''
    os.makedirs(path, exist_ok=True)

def batch_filename(batch_idx: int, batch_size: int, out_dir: str) -> str:
    '''
    Create filename for a raw deck batch stored as .npz.
    '''
    return os.path.join(out_dir, f'_rawDecks2_{batch_idx}_n={batch_size}.npz')

def gen_deck_arr(rng: random.Random) -> np.ndarray:
    '''
    Generate one deck as a (52,) uint8 array with exactly 26 zeros and 26 ones,
    shuffled without replacement.
    '''

    deck = np.array([0]*26 + [1]*26, dtype=np.uint8)
    rng.shuffle(deck) 
    return deck

def simulate_batch(batch_idx: int, batch_size: int, out_dir: str, seed: int = 12345) -> str:
    '''
    Generate one batch of raw decks (no scoring) and save as a single .npz:
      - array shape: (batch_size, 52), dtype=uint8, key='decks'
      - values: 0='R', 1='B'
    Returns the file path.
    '''
    ensure_dir(out_dir)
    rng = random.Random(seed + batch_idx)

    decks = np.empty((batch_size, 52), dtype=np.uint8)
    for i in range(batch_size):
        decks[i] = gen_deck_arr(rng)

    path = batch_filename(batch_idx, batch_size, out_dir)
    np.savez_compressed(path, decks=decks)

    return path

def perf_probe(out_dir: str, batch_size: int = 10_000, batches: int = 2, seed: int = 12345) -> dict:
    '''Time + size probe for generation-only pipeline.'''
    ensure_dir(out_dir)
    results = {'batch_idx': [], 'gen_write_time_s': [], 'file_mb': []}
    for b in range(batches):
        t0 = time.perf_counter()
        path = simulate_batch(b, batch_size, out_dir, seed=seed)
        t1 = time.perf_counter()
        size_mb = os.path.getsize(path) / (1024**2)
        results['batch_idx'].append(b)
        results['gen_write_time_s'].append(t1 - t0)
        results['file_mb'].append(round(size_mb, 4))
    with open(os.path.join(out_dir, 'perf_results2.json'), 'w') as f:
        json.dump(results, f, indent=2)

    return results
