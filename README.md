# Project Penney

## Description

Penney's Game is a two plater coin tossing game where each player will choose a sequence of heads (H) and tails (T) and the player with their sequence to first appear in the sequence of consecutive coin flips wins. Other variations of this game exist such as [Humble-Nishiyama Randomness Game](https://mathwo.github.io/assets/files/penney_game/humble-nishiyama_randomness_game-a_new_variation_on_penneys_coin_game.pdf)  which utilizes an ordinary deck of playing cards and follows the same format using red and black cards rather than heads and tails and the game iterates through the entire deck of cards.

## Quick-Start Guide

This project is managed using [UV](https://docs.astral.sh/uv/). If you do not yet have UV installed or need help troubleshooting issues with UV, refer to their [documentation](https://docs.astral.sh/uv/getting-started/features/). 

Once UV is installed, download the repository, navigate to the directory and run: `uv sync` to install dependencies.

Run the program
`uv run_tests.py`

## Contents
`run_tests.py` Contains the functions to run tests shown to the user.
`data_gen.py` Contains the functions and code used for generating a deck utilizing method 1 (described in `DataGeneration.md`)
`data_gen2.py` Contains the functions and code used for generating a deck utilizing method 2 (described in `DataGeneration.md`)
`raw_data` Contains the data generated (2 million entries)
