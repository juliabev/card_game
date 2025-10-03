Scoring.md: Describe, in words, how your scoring logic works. Provide simple examples if that helps improve clarity. Include a brief discussion of how you arrived at this method, what else you tried, and how you measured/compared approaches.
In an appropriate folder, include a .csv file that shows wins, draws, etc. by the two different scoring methods for the 56 valid combinations of player choices. This does not need to be run on the full set of 2M decks yet, it just needs to include enough data to show that it is working.


Julia's method:

The `score_ju.py` script implements a head-to-head scoring logic to determine the winner for each combination of players on each deck. The scoring is performed in a turn-based manner. For each deck, the script finds the first occurrence of either player's sequence. The player whose sequence appears first wins that "turn" and receives points based on the "card" (position of the match) and "trick" (number of matches) logic. The search then continues from that point in the deck for the next match.

At the end of each deck, the players' total "card" and "trick" scores are compared. The player with the higher score for "cards" gets a "card win" for that deck, and the same logic is applied to "tricks". If the scores are equal, the deck is counted as a "draw" for that category.

The script aggregates these wins and draws over all the decks, and the final output is a CSV file showing the total number of wins and draws for each player combination.

