### Data Generation

Kayla Aviles & Julia Beverley

#### Method 1:
Method 1 creates random decks by generated a numpy array of numpy arrays. Each card is encoded as 0 and 1s


#### Method 2:
Method 2 generates randomized decks and all possible combination match-ups and stores them in CSV files for later scoring and analysis. Each deck is built from 26 red (R) and 26 black (B) cards, shuffled randomly and stored as a string type. The decks are generated in batches, with 10,000 decks per file, to get 2 million decks at the end. The 


### Which method is preferred?
Method 1


Table 1.
| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |

method 1
  "total_decks": 500000,
  "batch_size": 20000,
  "n_batches": 25,
  "average_file_size": 0.1578,
  "average_time_per_file_s": 0.3995,
  "total_files_mb": 3.9441,
  "total_time_s": 9.9871
}

method 2
{
  "total_decks": 500000,
  "batch_size": 20000,
  "n_batches": 25,
  "average_file_size": 0.1578,
  "average_time_per_file_s": 0.4048,
  "total_files_mb": 3.9441,
  "total_time_s": 10.1203