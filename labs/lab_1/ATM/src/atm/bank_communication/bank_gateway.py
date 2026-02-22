from decimal import Decimal
from typing import Optional

from .mock_bank_repo import MockBankRepository
from .account_data import AccountData


class BankGateway:
    """Interface to the bank system (simulated via mock repository)."""

    def __init__(self) -> None:
        self._repo = MockBankRepository()

    def validate_pin(self, card_number: str, pin: str) -> bool:
        """Check if PIN is correct for the given card."""
        return self._repo.validate_pin(card_number, pin)

    def is_card_blocked(self, card_number: str) -> bool:
        """Check if the card is blocked."""
        account = self._repo.get_account(card_number)
        return account is not None and account.is_blocked

    def block_card(self, card_number: str) -> bool:
        """Block the card after too many failed attempts."""
        return self._repo.block_card(card_number)

    def get_balance(self, card_number: str) -> Optional[Decimal]:
        """Get current balance or None if card not found / blocked."""
        account = self._repo.get_account(card_number)
        if account and not account.is_blocked:
            return account.balance
        return None

    def withdraw(self, card_number: str, amount: Decimal) -> bool:
        """Withdraw money if possible."""
        balance = self.get_balance(card_number)
        if balance is None or balance < amount:
            return False
        return self._repo.update_balance(card_number, balance - amount)

    def deposit(self, card_number: str, amount: Decimal) -> bool:
        """Deposit money."""
        balance = self.get_balance(card_number)
        if balance is None:
            return False
        return self._repo.update_balance(card_number, balance + amount)

    def change_pin(self, card_number: str, new_pin: str) -> bool:
        """Change PIN via bank repository."""
        return self._repo.change_pin(card_number, new_pin)

    def get_account(self, card_number: str) -> Optional[AccountData]:
        """Get account data by card number (e.g. for expiry date)."""
        return self._repo.get_account(card_number)

    def transfer(
        self, from_card: str, to_card: str, amount: Decimal
    ) -> bool:
        """Transfer amount from one account to another."""
        return self._repo.transfer(from_card, to_card, amount)
