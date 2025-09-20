import numpy as np
import os, time, random, json

def ensure_dir(path: str):
    '''
    Ensure directory exists
    '''
    os.makedirs(path, exist_ok=True)

def batch_filename(batch_idx: int, batch_size: int, out_dir: str) -> str:
    '''
    Create filename for a raw deck batch stored as .npz
    '''
    return os.path.join(out_dir, f'_rawDecks2_{batch_idx}_n={batch_size}.npz')

def gen_deck_str(rng: random.Random) -> str:
    '''
    Generate 26 red + 26 black that are shuffled without replacement
    Return as 'R'/'B' string.
    '''
    deck = ['R'] * 26 + ['B'] * 26
    rng.shuffle(deck)

    return ''.join(deck)

def simulate_batch_str(batch_idx: int, batch_size: int, out_dir: str, seed: int = 12345) -> str:
    '''
    Generate one batch of raw string decks (no scoring) and save as a single .npz:
      - array shape: (batch_size,)
      - dtype: 'S52' (fixed-length byte string)
      - key: 'decks_str'
    Returns the file path.
    '''

    ensure_dir(out_dir)
    # each batch will have their own unique seed
    rng = random.Random(seed + batch_idx)

    # making 1D array of byte strings (S52).
    decks = np.empty((batch_size,), dtype='S52')
    for i in range(batch_size):
        s = gen_deck_str(rng)
        decks[i] = s.encode('ascii')

    path = batch_filename(batch_idx, batch_size, out_dir)
    np.savez_compressed(path, decks_str=decks)
    return path


# quantitative testing
# testing both file size and time
def time_size_testing(out_dir: str, batch_size: int = 10_000, batches: int = 2, seed: int = 12345) -> dict:
    '''
    Time + size testing.
    '''
    ensure_dir(out_dir)

    results = {'batch_idx': [], 'gen_write_time_s': [], 'file_mb': []}

    for b in range(batches):
        t0 = time.perf_counter()
        path = simulate_batch_str(b, batch_size, out_dir, seed=seed)
        t1 = time.perf_counter()
        size_mb = os.path.getsize(path) / (1024**2)
        results['batch_idx'].append(b)
        results['gen_write_time_s'].append(t1 - t0)
        results['file_mb'].append(round(size_mb, 4))

    with open(os.path.join(out_dir, 'perf_results2.json'), 'w') as f:
        json.dump(results, f, indent=2)

    return results
