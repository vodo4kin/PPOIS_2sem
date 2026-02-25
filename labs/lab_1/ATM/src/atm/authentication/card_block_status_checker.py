"""Check whether a card is blocked via the bank gateway."""

from ..bank_communication.bank_gateway import BankGateway


class CardBlockStatusChecker:
    """Checks if card is blocked via bank gateway."""

    def __init__(self, bank_gateway: BankGateway) -> None:
        """Store reference to bank gateway."""
        self._gateway = bank_gateway

    def is_blocked(self, card_number: str) -> bool:
        """Return True if card is blocked or not found."""
        return self._gateway.is_card_blocked(card_number)
