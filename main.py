from game_logic.deck import Deck
from game_logic.player import Player
from gameplay.engine import GameEngine

def main():
    print("Witaj w Pokerze 5-kartowym!")
    names = ["Ty", "Bot1", "Bot2", "Bot3"]
    players = Player.create_players(names, human_index=0)
    deck = Deck()
    engine = GameEngine(players, deck)

    while True:
        engine.play_round()
        print("\nStan żetonów:")
        for p in players:
            print(f"{p.name}: {p.stack} żetonów")
        cont = input("\nZagraj kolejną rundę? (t/n): ").lower()
        if cont != 't':
            print("Dziękujemy za grę!")
            break

if __name__ == "__main__":
    main()
