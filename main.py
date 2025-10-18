import src.data_gen as dg
import src.score as sc
import src.viz as viz
import json
import math
import time
import os

# --- Configuration ---
TOTAL_DECKS = 20_000
BATCH_SIZE = 10_000
RAW_DATA_DIR = './raw_data'
RESULTS_DIR = './results'
SEED = 12345
# -------------------

def augment_data(n: int):
    '''
    Generates n new decks, and automatically updates scores and figures.
    '''
    print(f'--- Augmenting data with {n} new decks ---')

    # 1. Data Generation
    dg.ensure_dir(RAW_DATA_DIR)
    n_batches = math.ceil(n / BATCH_SIZE)
    prod = 0

    # Find the next available batch index
    raw_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.npz')]
    next_batch_idx = len(raw_files)

    for b in range(n_batches):
        this_size = min(BATCH_SIZE, n - prod)
        batch_idx = next_batch_idx + b
        dg.simulate_batch(
            batch_idx=batch_idx,
            batch_size=this_size,
            out_dir=RAW_DATA_DIR,
            seed=SEED + batch_idx # Use a new seed for each batch
        )
        prod += this_size

    print(f'--- {n} new decks generated in {n_batches} batches ---')

    # 2. Scoring
    print('\n--- Re-running Scoring ---')
    output_csv_path = os.path.join(RESULTS_DIR, 'scoring_results.csv')
    total_decks = sc.run_simulation(RAW_DATA_DIR, output_csv_path)
    print('--- Scoring Complete ---')

    # 3. Visualization
    print('\n--- Re-generating Visualizations ---')
    viz.run_visualization(csv_path=output_csv_path, outdir=RESULTS_DIR, total_decks=total_decks)
    print('--- Visualizations Complete ---')


import argparse

def run_full_process():
    '''
    This script serves as the main entry point to run the full project pipeline.
    It orchestrates the following steps:
    1. Generates simulated card deck data.
    2. Runs the scoring simulation on the generated data.
    3. Creates and saves heatmap visualizations of the results.
    '''
    # --- 1. Data Generation ---
    print('--- Step 1: Generating Data ---')
    dg.ensure_dir(RAW_DATA_DIR)
    n_batches = math.ceil(TOTAL_DECKS / BATCH_SIZE)
    prod = 0

    gen_results = {'batch_idx': [], 'gen_write_time_s': [], 'file_mb': []}

    for b in range(n_batches):
        this_size = min(BATCH_SIZE, TOTAL_DECKS - prod)
        t0 = time.perf_counter()
        path = dg.simulate_batch(b, this_size, RAW_DATA_DIR, seed=SEED + b)
        t1 = time.perf_counter()
        size_mb = os.path.getsize(path) / (1024**2)

        gen_results['batch_idx'].append(b)
        gen_results['gen_write_time_s'].append(t1 - t0)
        gen_results['file_mb'].append(size_mb)

        prod += this_size

    with open(os.path.join(RAW_DATA_DIR, 'perf_results.json'), 'w') as f:
        json.dump(gen_results, f, indent=2)
    
    print(f'Successfully generated {TOTAL_DECKS} decks in {n_batches} batches.')

    # --- 2. Scoring ---
    print('\n--- Step 2: Running Scoring Simulation ---')
    dg.ensure_dir(RESULTS_DIR)
    output_csv_path = os.path.join(RESULTS_DIR, 'scoring_results.csv')
    total_decks = sc.run_simulation(RAW_DATA_DIR, output_csv_path)

    # --- 3. Visualization ---
    print('\n--- Step 3: Generating Visualizations ---')
    viz.run_visualization(csv_path=output_csv_path, outdir=RESULTS_DIR, total_decks=total_decks)

    print('\n--- Pipeline Finished ---')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the card game simulation pipeline.")
    parser.add_argument('--augment', type=int, metavar='N', help='Generate N new decks and update scores and figures.')

    args = parser.parse_args()

    if args.augment:
        augment_data(args.augment)
    else:
        run_full_process()