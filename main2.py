import math
import method2 as m2


TOTAL_DECKS = 2_000_000
BATCH_SIZE = 10_000
OUT_DIR = "Data"

# gen batches
for i in range(math.ceil(TOTAL_DECKS / BATCH_SIZE)):
    print(f"Running batch {i+1}/{TOTAL_DECKS//BATCH_SIZE} ...")
    m2.simulate_batch(i, BATCH_SIZE, OUT_DIR)

# summarize results
print("All batches complete. Creating summary.json ...")
m2.summarize(OUT_DIR)
print("Summary written to Data/summary.json")
