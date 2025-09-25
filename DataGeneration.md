# Data Generation
---
Kayla Aviles & Julia Beverley


#### Method 1:
Method 1 creates random decks by generated a numpy array of numpy arrays. Each card is encoded as 0 and 1s, so 26 zeros and 26 ones, which are then shuffled into a random order. The decks are stored in a 2D numpy array and the filenames are automatically created.


#### Method 2:
Method 2 generates randomized decks and all possible combination match-ups and stores them in CSV files for later scoring and analysis. Each deck is built from 26x red (R) and 26 black (B) cards, shuffled randomly and stored as a string type. The decks are generated in batches, with 10,000 decks per file, to get 2 million decks at the end. 


### Which method is preferred?
Method 1 is preferred as the average time per file and total time is shorter. Method 1 also stores the decks in numpy arrays as integers, which is a lot more effective when it comes to data generation and storage.


Table 1. Quantitative Testing (Time & File Size)

| Metric                | Method 1 | Method 2 |
| --------------------- | -------- | -------- |
<<<<<<< Updated upstream
| Avg File Size (MB)    |  0.0791  | 0.0791   | 
| Total File Size (MB)  | 15.8108  | 15.8108  |
| Avg Time Per File (s) |  0.1107  |  0.196   |
| Total Time (s)        | 22.135   |  39.197  |
=======
| Avg File Size (MB)    | 0.0791   | 0.0791   |
| Total File Size (MB)  | 15.8108  | 15.8132  |
| Avg Time Per File (s) | 0.0802   | 0.1248   |
| Total Time (s)        | 16.0472  | 24.9645  |