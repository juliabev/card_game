import math
import analysis2 as a2

TOTAL_DECKS = 2_000_000
BATCH_SIZE = 10_000
OUT_DIR = "Data"

# gen batches
for i in range(math.ceil(TOTAL_DECKS / BATCH_SIZE)):
    print(f"Running batch {i+1}/{math.ceil(TOTAL_DECKS / BATCH_SIZE)} ...")
    a2.simulate_batch(i, BATCH_SIZE, OUT_DIR)

# summarize results
print("All batches complete. Creating summary file...")
a2.summarize(OUT_DIR)
print("Summary written to Data/summary.csv")