from deck import *
from player import *



if __name__ == "__main__":
    d = deck()
    d.print_cards()
    print("\n\n")
    d.shuffle()
    d.print_cards()

    p = player()
    p.get_hand(d)

    p.print_hand()

    print("hello world")