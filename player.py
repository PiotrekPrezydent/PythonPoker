class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)