from card import *
import random


class deck:
    def __init__(self):
        self.cards = []
        colors = ["spades","hearts","diamonds","clubs"]
        ranks = ["ace","2","3","4","5","6","7","8","9","10","jack","queen","king"]
        for rank in ranks:
            for color in colors:
                self.cards.append(card(rank,color))
        pass

    def shuffle(self):
        if self.cards == []:
            print("deck is empty")
            return
        
        random.shuffle(self.cards)
        pass

    def print_cards(self):
        if self.cards == []:
            print("deck is empty")
            return
        
        for card in self.cards:
            card.show()

        pass

    def take_cards(self, number) -> list:
        returned = []
        for i in range(0,number):
            returned.append(self.cards.pop)
        return returned

    def store_cards(self, cards):
        self.cards.insert(cards)
        pass
