Scoring.md Instructions: Describe, in words, how your scoring logic works. Provide simple examples if that helps improve clarity. Include a brief discussion of how you arrived at this method, what else you tried, and how you measured/compared approaches.
In an appropriate folder, include a .csv file that shows wins, draws, etc. by the two different scoring methods for the 56 valid combinations of player choices. This does not need to be run on the full set of 2M decks yet, it just needs to include enough data to show that it is working.



*Method 1*:

The `score_1.py` script implements a head-to-head scoring logic to determine the winner for each combination of players on each deck. The scoring is performed in a turn-based manner: the script scans a deck left-to-right and when a player’s 3-bit sequence is matched that player wins the current turn and receives points based on the number of cards captured by that match (i.e., the cards removed from play when the sequence is matched) and the trick count (one trick per matched sequence). The search then continues from the point after the captured cards for the next match. At the end of each deck, the players’ total card and trick scores are compared; the player with the higher cards total receives a card win for that deck (and similarly for tricks), while equal totals are recorded as draws. The script aggregates these wins and draws across all decks and writes the final summary to a CSV file (`scoring_results1.csv`).


*Method 2*:

The `score_2.py` script uses a greedy, sequential scoring method to simulate the Humble-Nishiyama randomness game. It processes each deck for every pair of players to determine a winner. The accumulation of a pile is when a "pile" of cards starts at 2. For every card dealt from the deck (for each 3-card window examined), the pile grows by one. In method 2, it checks the current 3-card window for a match with either player's sequence. The first player whose sequence appears wins the current pile. The size of the pile is added to their "cards won" score, and their "tricks won" count is incremented by one. After a trick is won, the pile count is reset to 2. The three cards that formed the winning sequence are considered "removed" by advancing the scanner 3 positions down the deck. This prevents the same cards from being scored in an overlapping sequence.

This process is repeated for all 56 unique player pairings across all available decks. The final output is a CSV file (`scoring_results2.csv`) that aggregates the total cards and tricks won by each player, the number of games won, lost, or tied, and the corresponding win/loss/tie rates. This method differs from Julia's by simulating a dynamic, accumulating pile and a "first-come, first-served" trick-winning mechanism, rather than resolving all matches at the end.                     


 Table 1. Quantitative Testing (Time & Memory Usage)

| Metric                     | Method 1 | Method 2 |
|:---------------------------|---------:|---------:|
| Execution Time (s)         | 2625.33 |   253.86 |
| Current Memory Usage (MB)  |     0.68 |     0.03 |

