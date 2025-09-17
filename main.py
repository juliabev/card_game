def main():
    print("Hello from card-game!")
    print("Hi from Kayla & Julia")
    


if __name__ == "__main__":
    main()


from analysis import getp1combo, getp2combo, shuffle, cardgame
import random

p1 = getp1combo()
p2 = getp2combo(p1)

print(p1)
print(p2)

full_deck = [0]*26 + [1]*26

deck = shuffle(full_deck)
print(deck)

p1_tricks, p2_tricks, p1_points, p2_points = cardgame(deck, p1, p2)
print(f'Final point scores: Player 1 has {p1_tricks} tricks, Player 2 has {p2_tricks} tricks. Player 1 has {p1_points} points, and Player 2 has {p2_points} points.')