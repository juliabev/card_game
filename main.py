def main():
    print("Hello from card-game!")
    print("Hi from Kayla & Julia")
    


if __name__ == "__main__":
    main()


from analysis import getp1combo, getp2combo, shuffle, cardgame, simulate, generate_deck_files, run_cardgame_on_files
import random

p1 = getp1combo()
p2 = getp2combo(p1)

#print(p1)
#print(p2)

full_deck = ['R']*26 + ['B']*26

generate_deck_files(full_deck)

p1_options = [["R","R","R"],
            ["R","R","B"],
            ["R","B","R"],
            ["R","B","B"],
            ["B","R","R"],
            ["B","R","B"],
            ["B","B","R"],
            ["B","B","B"]]

p2_options = [["R","R","R"],
            ["R","R","B"],
            ["R","B","R"],
            ["R","B","B"],
            ["B","R","R"],
            ["B","R","B"],
            ["B","B","R"],
            ["B","B","B"]]

run_cardgame_on_files(1,1,p1_options=p1_options, p2_options=p2_options)

#p1_tricks, p2_tricks, p1_points, p2_points = cardgame(deck, p1, p2)
#print(f'Final point scores: Player 1 has {p1_tricks} tricks, Player 2 has {p2_tricks} tricks. Player 1 has {p1_points} points, and Player 2 has {p2_points} points.')\

results = simulate(1, full_deck, p1, p2)
print(results)
