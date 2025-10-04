Scoring.md Instructions: Describe, in words, how your scoring logic works. Provide simple examples if that helps improve clarity. Include a brief discussion of how you arrived at this method, what else you tried, and how you measured/compared approaches.
In an appropriate folder, include a .csv file that shows wins, draws, etc. by the two different scoring methods for the 56 valid combinations of player choices. This does not need to be run on the full set of 2M decks yet, it just needs to include enough data to show that it is working.



*Method 1*:

The `score_1.py` script implements a head-to-head scoring logic to determine the winner for each combination of players on each deck. The scoring is performed in a turn-based manner. For each deck, the script finds the first occurrence of either player's sequence. The player whose sequence appears first wins that "turn" and receives points based on the "card" (position of the match) and "trick" (number of matches) logic. The search then continues from that point in the deck for the next match.

At the end of each deck, the players' total "card" and "trick" scores are compared. The player with the higher score for "cards" gets a "card win" for that deck, and the same logic is applied to "tricks". If the scores are equal, the deck is counted as a "draw" for that category.

The script aggregates these wins and draws over all the decks, and the final output is a CSV file showing the total number of wins and draws for each player combination.


*Method 2*:

The `score_2.py` script uses a greedy, sequential scoring method to simulate the Humble-Nishiyama randomness game. It processes each deck for every pair of players to determine a winner. The accumulation of a pile is when a "pile" of cards starts at 2. For every card dealt from the deck (for each 3-card window examined), the pile grows by one. In method 2, it checks the current 3-card window for a match with either player's sequence. The first player whose sequence appears wins the current pile. The size of the pile is added to their "cards won" score, and their "tricks won" count is incremented by one. After a trick is won, the pile count is reset to 2. The three cards that formed the winning sequence are considered "removed" by advancing the scanner 3 positions down the deck. This prevents the same cards from being scored in an overlapping sequence.

This process is repeated for all 56 unique player pairings across all available decks. The final output is a CSV file (`scoring_results2.csv`) that aggregates the total cards and tricks won by each player, the number of games won, lost, or tied, and the corresponding win/loss/tie rates. This method differs from Julia's by simulating a dynamic, accumulating pile and a "first-come, first-served" trick-winning mechanism, rather than resolving all matches at the end.                     


 Table 1. Quantitative Testing (Time & Memory Usage)

| Metric                     | Method 1 | Method 2 |
|:---------------------------|---------:|---------:|
| Execution Time (s)         | 2625.33 |   253.86 |
| Current Memory Usage (MB)  |     0.68 |     0.03 |

