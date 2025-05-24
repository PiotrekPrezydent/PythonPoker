import random
from game_logic.card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.suits for rank in Card.ranks]
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def discard_to_bottom(self, card):
        self.cards.insert(0, card)

    def deal(self, players, num_cards=5):
        for _ in range(num_cards):
            for player in players:
                player.hand.append(self.draw())

    def __str__(self):
        return f"Deck with {len(self.cards)} cards remaining."
