## Visualization Instructions

Include the sample size in the title
Make sure the title includes which scoring method (By Tricks or By Cards)
Respect the ordering of the rows/columns. I'm just counting up in binary (B=0, R=1) from top to bottom, left to right.
Format the probabilities like I have: Win(Draw), both integers.
My cells are colored by the win probability
The vertical axis should be "Opponent choice", the horizontal axis is "My choice"
(New) Put a black box around the cell with the highest win probability in each row.


The code should include a function called augment_data(n: int). The function should create n new decks, and automatically update scores and figures.

## viz.py

This file generates heatmap visualizations that show how often a player wins or ties across all deck combinations. It is implemented after data generation, then scoring, and it can be used again with augment_data. The visualization script reads the CSV summary file created by the scoring, and produces two heatmaps:
1. Win rate by cards
2. Win rate by tricks

Both maps show "my choice" and "opponent's choice" of sequence. The numbers in each cell show the win percentage (and draws in parentheses). The black outlined box is the highest win probability in that row. 
