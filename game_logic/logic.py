from game_logic.card import Card
from collections import Counter

RANK_VALUES = {r: i for i, r in enumerate(Card.ranks)}

def exchange_cards(hand, indices, deck):
    if any(i < 0 or i >= len(hand) for i in indices):
        raise IndexError("Nieprawidłowy indeks karty do wymiany")
    new_cards = [deck.draw() for _ in indices]
    for i, idx in enumerate(indices):
        old_card = hand[idx]
        deck.discard_to_bottom(old_card)
        hand[idx] = new_cards[i]
    return hand

def hand_rank(hand):
    ranks = sorted([card.rank for card in hand], key=lambda r: RANK_VALUES[r], reverse=True)
    suits = [card.suit for card in hand]
    counts = Counter(ranks)
    values = sorted(counts.values(), reverse=True)
    unique_ranks = sorted(set(ranks), key=lambda r: RANK_VALUES[r], reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = all(RANK_VALUES[ranks[i]] - RANK_VALUES[ranks[i + 1]] == 1 for i in range(4))

    if is_flush and ranks == ['A', 'K', 'Q', 'J', '10']:
        return (9, ranks)  # Poker królewski
    elif is_flush and is_straight:
        return (8, ranks)  # Poker
    elif values == [4, 1]:
        return (7, ranks)  # Kareta
    elif values == [3, 2]:
        return (6, ranks)  # Full
    elif is_flush:
        return (5, ranks)
    elif is_straight:
        return (4, ranks)
    elif values == [3, 1, 1]:
        return (3, ranks)
    elif values == [2, 2, 1]:
        return (2, ranks)
    elif values == [2, 1, 1, 1]:
        return (1, ranks)
    else:
        return (0, ranks)  # High card
