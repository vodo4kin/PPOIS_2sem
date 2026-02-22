from typing import Optional

from ..bank_communication.bank_gateway import BankGateway
from .pin_validator import PinValidator
from .card_block_status_checker import CardBlockStatusChecker
from ..config import Config


class AuthenticationService:
    """Handles card authentication and PIN attempts."""

    def __init__(self, bank_gateway: BankGateway) -> None:
        self._gateway = bank_gateway
        self._pin_validator = PinValidator()
        self._block_checker = CardBlockStatusChecker(bank_gateway)
        self._attempts_left: dict[str, int] = {}  # card_number -> attempts

    def authenticate(self, card_number: str, pin: str) -> bool:
        """Try to authenticate user with PIN."""
        if self._block_checker.is_blocked(card_number):
            return False

        if not self._pin_validator.is_valid_format(pin):
            return False

        if card_number not in self._attempts_left:
            self._attempts_left[card_number] = Config.MAX_PIN_ATTEMPTS

        if self._gateway.validate_pin(card_number, pin):
            self._attempts_left[card_number] = Config.MAX_PIN_ATTEMPTS
            return True

        self._attempts_left[card_number] -= 1
        remaining = self._attempts_left[card_number]

        if remaining <= 0:
            self._gateway.block_card(card_number)
            del self._attempts_left[card_number]

        return False

    def get_attempts_left(self, card_number: str) -> Optional[int]:
        return self._attempts_left.get(card_number)
