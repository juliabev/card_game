import data_gen as dg
import data_gen2 as dg2
import json
import math
import time
import os

TOTAL_DECKS = 2_000_000
BATCH_SIZE = 10_000
OUT_DIR = './raw_data'
SEED = 12345

if __name__ == '__main__':

    dg.ensure_dir(OUT_DIR)
    n_batches = math.ceil(TOTAL_DECKS / BATCH_SIZE)
    prod = 0

    results = {'batch_idx': [], 'gen_write_time_s': [], 'file_mb': []}

    for b in range(n_batches):
        this_size = min(BATCH_SIZE, TOTAL_DECKS - prod)
        t0 = time.perf_counter()
        path = dg.simulate_batch(b, this_size, OUT_DIR, seed=SEED)
        t1 = time.perf_counter()
        size_mb = os.path.getsize(path) / (1024**2)

        results['batch_idx'].append(b)
        results['gen_write_time_s'].append(t1 - t0)
        results['file_mb'].append(size_mb)

        prod += this_size

    with open(os.path.join(OUT_DIR, 'perf_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    print(json.dumps({
        'total_decks': TOTAL_DECKS,
        'batch_size': BATCH_SIZE,
        'n_batches': n_batches,
        'average_file_size': round((sum(results['file_mb'])/n_batches), 4),
        'average_time_per_file_s': round((sum(results['gen_write_time_s'])/n_batches), 4),
        'total_files_mb': round(sum(results['file_mb']), 4),
        'total_time_s': round(sum(results['gen_write_time_s']), 4)
    }, indent=2))


    dg2.ensure_dir(OUT_DIR)
    n_batches = math.ceil(TOTAL_DECKS / BATCH_SIZE)
    prod = 0

    results2 = {'batch_idx': [], 'gen_write_time_s': [], 'file_mb': []}

    for b in range(n_batches):
        this_size = min(BATCH_SIZE, TOTAL_DECKS - prod)
        t0 = time.perf_counter()
        path = dg2.simulate_batch_str(b, this_size, OUT_DIR, seed=SEED)
        t1 = time.perf_counter()
        size_mb = os.path.getsize(path) / (1024**2)

        results2['batch_idx'].append(b)
        results2['gen_write_time_s'].append(t1 - t0)
        results2['file_mb'].append(size_mb)

        prod += this_size

    with open(os.path.join(OUT_DIR, 'perf_results2.json'), 'w') as f:
        json.dump(results2, f, indent=2)

    print(json.dumps({
        'total_decks': TOTAL_DECKS,
        'batch_size': BATCH_SIZE,
        'n_batches': n_batches,
        'average_file_size': round((sum(results2['file_mb'])/n_batches), 4),
        'average_time_per_file_s': round((sum(results2['gen_write_time_s'])/n_batches), 4),
        'total_files_mb': round(sum(results2['file_mb']), 4),
        'total_time_s': round(sum(results2['gen_write_time_s']), 4)
    }, indent=2))

