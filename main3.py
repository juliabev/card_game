import math
import analysis3 as an

TOTAL_DECKS = 2_000_000
BATCH_SIZE = 10_000
OUT_DIR = "Data"

# gen batches
for i in range(math.ceil(TOTAL_DECKS / BATCH_SIZE)):
    print(f"Running batch {i+1}/{math.ceil(TOTAL_DECKS / BATCH_SIZE)} ...")
    an.simulate_batch(i, BATCH_SIZE, OUT_DIR)

# summarize results
print("All batches complete. Creating summary file...")
an.summarize(OUT_DIR)
print("Summary written to Data/summary.csv")