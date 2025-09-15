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

cardgame(deck, p1, p2)
