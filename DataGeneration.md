### Data Generation

Kayla Aviles & Julia Beverley

#### Method 1:
Method 1 creates random decks by generated a numpy array of numpy arrays. Each card is encoded as 0 and 1s


#### Method 2:
Method 2 generates randomized decks and all possible combination match-ups and stores them in CSV files for later scoring and analysis. Each deck is built from 26x red (R) and 26 black (B) cards, shuffled randomly and stored as a string type. The decks are generated in batches, with 10,000 decks per file, to get 2 million decks at the end. The 


### Which method is preferred?
Method 1


| Metric                | Method 1 | Method 2 |
| --------------------- | -------- | -------- |
| Avg File Size (MB)    | 0.1578   | 0.1578   |
| Total File Size (MB)  | 3.9441   | 3.9441   |
| Avg Time Per File (s) | 0.3995   | 0.4048   |
| Total Time (s)        | 9.9871   | 10.1203  |
