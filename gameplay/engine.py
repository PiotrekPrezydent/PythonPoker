from typing import List
from game_logic.card import Card
from game_logic.player import Player
from game_logic.deck import Deck
from data.logger import save_game_result, save_game_log

class GameEngine:
    def __init__(self, players: List[Player], deck: Deck):
        self.players = players
        self.deck = deck
        self.pot = 0
        self.current_bet = 0
        self.round_num = 1
        self.game_log = []

    def reset_round(self):
        self.pot = 0
        self.current_bet = 0
        for p in self.players:
            p.hand = []
            p.is_active = True
            p.current_bet = 0

    def deal_cards(self):
        self.deck.shuffle()
        # Metoda deal przyjmuje listę graczy i liczbę kart
        self.deck.deal(self.players, 5)

    def betting_round(self):
        print("\n-- Runda zakładów --")
        active_players = [p for p in self.players if p.is_active and p.stack > 0]
        idx = 0
        while True:
            if not active_players:
                break  # brak aktywnych graczy
            
            player = active_players[idx % len(active_players)]
            if not player.is_active or player.stack == 0:
                idx += 1
                continue

            print(f"\n{player.name}, twoje karty: {player.cards_to_str()}")
            print(f"Obecna pula: {self.pot}, obecny zakład: {self.current_bet}, Twój stack: {player.stack}")

            action = None
            if player.is_human:
                while True:
                    try:
                        raw = input("Wybierz akcję (check/call/raise/fold): ").lower()
                        if raw not in ["check", "call", "raise", "fold"]:
                            raise ValueError("Nieprawidłowa akcja.")
                        action = raw
                        break
                    except ValueError as e:
                        print(e)
            else:
                action = player.choose_action(self.current_bet)
                print(f"Bot {player.name} wybiera: {action}")

            if action == "fold":
                player.is_active = False
                self.game_log.append(f"{player.name} spasował.")
                active_players = [p for p in self.players if p.is_active and p.stack > 0]
                if len(active_players) <= 1:
                    break
            elif action == "check":
                if self.current_bet == player.current_bet:
                    self.game_log.append(f"{player.name} wykonał check.")
                else:
                    print("Nie możesz checkować, musisz przynajmniej wyrównać.")
                    continue
            elif action == "call":
                to_call = self.current_bet - player.current_bet
                if to_call > player.stack:
                    print(f"{player.name} nie ma wystarczających środków na call, musi spasować lub podbić mniejszą kwotę.")
                    continue
                player.stack -= to_call
                player.current_bet += to_call
                self.pot += to_call
                self.game_log.append(f"{player.name} wyrównał zakład o {to_call}.")
            elif action == "raise":
                try:
                    if player.is_human:
                        amount = int(input("Podaj kwotę podbicia (min 50): "))
                    else:
                        amount = 50  # bot podbija o minimalną kwotę
                    if amount < 50:
                        print("Minimalne podbicie to 50.")
                        continue
                    to_call = self.current_bet - player.current_bet
                    total_bet = to_call + amount
                    if total_bet > player.stack:
                        print("Nie masz wystarczających środków na podbicie tej kwoty.")
                        continue
                    player.stack -= total_bet
                    player.current_bet += total_bet
                    self.current_bet += amount
                    self.pot += total_bet
                    self.game_log.append(f"{player.name} podbił zakład o {amount}.")
                    active_players = [p for p in self.players if p.is_active and p.stack > 0]
                except ValueError as e:
                    print(e)
                    continue

            # Sprawdzenie warunku zakończenia rundy
            active_bets = [p.current_bet for p in active_players if p.is_active]
            if len(active_bets) > 0 and len(set(active_bets)) == 1:
                break

            idx += 1

    def showdown(self):
        print("\n-- Showdown --")
        active_players = [p for p in self.players if p.is_active]
        for p in active_players:
            print(f"{p.name}: {p.cards_to_str()} - Ranking: {p.hand_rank()}")

        winner = max(active_players, key=lambda p: p.hand_rank())
        print(f"\nZwycięzca rundy: {winner.name}, zdobywa pulę {self.pot} żetonów.")
        winner.stack += self.pot
        self.game_log.append(f"Zwycięzca rundy: {winner.name}, pula: {self.pot}.")
        save_game_result(winner.name, self.pot, self.round_num)
        save_game_log(self.game_log)

    def play_round(self):
        self.reset_round()
        self.deal_cards()
        self.betting_round()
        self.showdown()
        self.round_num += 1
