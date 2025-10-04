import os
import glob
from src.data_gen import time_size_testing
# from src.score import score_raw_batch, summarize

def main():
    '''
    This script runs the full data generation and scoring pipeline.
    '''
    # Define directories
    raw_data_dir = 'raw_data'
    scored_data_dir = 'scored_data'

    # --- Step 1: Generate raw deck data ---
    print('--- Running Data Generation ---')
    # For testing, let's generate 2 batches of 100 decks each
    time_size_testing(raw_data_dir, batch_size=100, batches=2)
    print(f'Data generation complete. Raw data saved in {raw_data_dir}')

    # --- Step 2: Score the raw deck data ---
    print('\n--- Scoring Raw Data ---')
    raw_files = glob.glob(os.path.join(raw_data_dir, '*.npz'))
    if not raw_files:
        print('No raw data files found to score.')
    else:
        for file_path in raw_files:
            print(f'Scoring {file_path}...')
            score_raw_batch(file_path, scored_data_dir)
        print(f'Scoring complete. Scored data saved in {scored_data_dir}')

    # --- Step 3: Generate the final summary ---
    print('\n--- Generating Final Summary ---')
    summary_path = summarize(scored_data_dir)
    print(f'Summary complete. Final summary saved to {summary_path}')

if __name__ == '__main__':
    main()