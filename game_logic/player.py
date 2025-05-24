from typing import List, Optional
from game_logic.card import Card
from game_logic.logic import hand_rank

class Player:
    def __init__(self, name: str, stack: int = 1000, is_human: bool = False):
        self.name = name
        self.hand: List[Card] = []
        self._stack = stack
        self.is_human = is_human
        self.is_active = True  # Czy gracz jest w grze (nie spasował)
        self.current_bet = 0   # Kwota postawiona w bieżącej rundzie

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, value):
        if value < 0:
            raise ValueError("Stack nie może być ujemny.")
        self._stack = value

    def cards_to_str(self):
        return ', '.join(str(card) for card in self.hand)

    def hand_rank(self):
        return hand_rank(self.hand)

    def choose_cards_to_exchange(self):
        # Prosty bot: losowo wymienia 0–2 kart
        import random
        indices = random.sample(range(5), random.randint(0, 2))
        return indices

    def check(self, current_bet: int) -> str:
        # Check możliwy tylko, gdy current_bet == self.current_bet (brak podbicia)
        if current_bet == self.current_bet:
            return "check"
        else:
            return "call"  # Jeśli jest podbicie, to call

    def call(self, current_bet: int) -> int:
        # Różnica do dopłacenia
        to_call = current_bet - self.current_bet
        if to_call > self.stack:
            raise ValueError("Insufficient funds to call")
        self.stack -= to_call
        self.current_bet += to_call
        return to_call

    def raise_bet(self, current_bet: int, raise_amount: int) -> int:
        total_bet = current_bet + raise_amount
        to_raise = total_bet - self.current_bet
        if to_raise > self.stack:
            raise ValueError("Insufficient funds to raise")
        self.stack -= to_raise
        self.current_bet += to_raise
        return to_raise

    def fold(self):
        self.is_active = False

    def choose_action(self, current_bet: int, min_raise: int = 50) -> str:
        """
        Dla bota - prosta heurystyka decyzyjna:
        - Jeśli ręka silna (np. rank poniżej 3) to raise
        - Jeśli średnia, call
        - Słaba, fold
        Dla gracza - zwraca None, bo decyzję podejmuje użytkownik (GUI/CLI)
        """
        if self.is_human:
            return None  # decyzję musi podjąć użytkownik z interfejsu

        rank = self.hand_rank()
        # rank to krotka np. (2, [...]) - im mniejsze pierwsze, tym silniejsza ręka
        if rank[0] <= 3:  # np. poker królewski, kareta, full house
            return "raise"
        elif rank[0] <= 6:
            return "call"
        else:
            return "fold"

    @classmethod
    def create_players(cls, names: List[str], human_index: int = 0):
        return [cls(name, is_human=(i == human_index)) for i, name in enumerate(names)]
