from typing import List

from .card import Card


class CardRetainer:
    """Stores retained (swallowed) cards."""

    def __init__(self) -> None:
        self._retained: List[Card] = []

    def retain(self, card: Card) -> None:
        """Add card to retained bin."""
        self._retained.append(card)

    def get_retained_count(self) -> int:
        return len(self._retained)

    def get_retained_card_numbers(self) -> List[str]:
        """Return card numbers currently in the retainer (for technician display)."""
        return [card.number for card in self._retained]
