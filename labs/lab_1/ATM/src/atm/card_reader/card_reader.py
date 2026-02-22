from typing import Optional

from .card import Card
from .card_retainer import CardRetainer


class CardReader:
    """Simulates card insertion and reading."""

    def __init__(self) -> None:
        self._current_card: Optional[Card] = None
        self._retainer = CardRetainer()

    def insert_card(self, card_number: str) -> Optional[Card]:
        """Simulate card insertion."""
        if self._current_card is not None:
            raise RuntimeError("Another card is already inserted")
        try:
            card = Card(number=card_number)
            self._current_card = card
            return card
        except ValueError as e:
            raise ValueError(f"Invalid card: {e}") from e

    def eject_card(self) -> None:
        """Eject current card."""
        self._current_card = None

    def retain_card(self) -> None:
        """Retain (swallow) the card - e.g. after too many wrong PINs."""
        if self._current_card:
            self._retainer.retain(self._current_card)
            self._current_card = None

    def get_current_card(self) -> Optional[Card]:
        return self._current_card
