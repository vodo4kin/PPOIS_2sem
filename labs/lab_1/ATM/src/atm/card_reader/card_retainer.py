"""Storage for cards retained (swallowed) by the ATM."""

from .card import Card


class CardRetainer:
    """Stores retained (swallowed) cards."""

    def __init__(self) -> None:
        """Create empty retainer."""
        self._retained: list[Card] = []

    def retain(self, card: Card) -> None:
        """Add card to retained bin."""
        self._retained.append(card)

    def get_retained_count(self) -> int:
        """Return number of cards currently retained."""
        return len(self._retained)

    def get_retained_card_numbers(self) -> list[str]:
        """Return card numbers currently in the retainer (for technician display)."""
        return [card.number for card in self._retained]
