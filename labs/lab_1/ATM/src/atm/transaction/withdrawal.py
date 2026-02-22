from decimal import Decimal
from typing import TYPE_CHECKING

from .transaction import Transaction
from ..config import Config

if TYPE_CHECKING:
    from ..atm import ATM


class WithdrawalTransaction(Transaction):
    """Transaction for cash withdrawal."""

    def __init__(self, atm: "ATM", amount: Decimal) -> None:
        super().__init__(atm, amount=amount)

    def execute(self) -> bool:
        if self.amount is None:
            raise RuntimeError("Withdrawal amount is required")

        if self.amount <= 0:
            self.error_message = "Amount must be positive"
            return False

        if self.amount % 100 != 0:
            self.error_message = "Amount must be multiple of 100"
            return False

        if self.amount < Config.MIN_WITHDRAW_AMOUNT:
            self.error_message = f"Minimum withdrawal: {Config.MIN_WITHDRAW_AMOUNT}"
            return False

        card = self.atm.card_reader.get_current_card()
        if card is None:
            self.error_message = "No card inserted"
            return False

        if not self.atm.bank_gateway.withdraw(card.number, self.amount):
            self.error_message = "Insufficient funds or withdrawal failed"
            return False

        # Пытаемся выдать наличные
        try:
            self.atm.cash_dispenser.dispense(int(self.amount))
            self.atm.display.show_message(
                f"Take your {self.amount} {Config.DEFAULT_CURRENCY}")
            self.success = True
            self.log_transaction()
            return True
        except ValueError as e:
            # Откатываем списание (в реальности — сложнее)
            self.atm.bank_gateway.deposit(card.number, self.amount)
            self.error_message = str(e)
            self.atm.display.show_message(
                "Cash dispenser error. Transaction cancelled.")
            return False
