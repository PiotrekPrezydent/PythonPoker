from deck import Deck
from player import Player

deck = Deck()
deck.shuffle()

players = [Player("Alice"), Player("Bob")]
deck.deal(players, 5)

for player in players:
    print(f"{player.name}'s hand: {player.show_hand()}")