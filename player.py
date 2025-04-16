from deck import *
from typing import List

class player:
    def __init__(self):
        self.hand : List[card] = []
        pass

    def get_hand(self,deck : deck):
        self.hand = deck.take_cards(5)

    def return_cards(self, deck : deck):
        deck.take_cards(self.hand)

    def exchange(self, index, deck : deck):
        deck.storeCards(self.hand[index])
        self.hand.append(deck.take_cards(1))


    def print_hand(self):
        for c in self.hand:
            print(c)
            print("\t")


