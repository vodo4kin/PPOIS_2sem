from decimal import Decimal
from typing import TYPE_CHECKING

from .transaction import Transaction
from ..config import Config

if TYPE_CHECKING:
    from ..atm import ATM


class PaymentTransaction(Transaction):
    """Transaction for paying a service (utility, etc.)."""

    def __init__(
        self, atm: "ATM", amount: Decimal, service_name: str
    ) -> None:
        super().__init__(atm, amount=amount)
        self.service_name = service_name

    def execute(self) -> bool:
        if self.amount is None or self.amount <= 0:
            self.error_message = "Amount must be positive"
            return False

        card = self.atm.card_reader.get_current_card()
        if card is None:
            self.error_message = "No card inserted"
            return False

        if not self.atm.bank_gateway.withdraw(card.number, self.amount):
            self.error_message = "Insufficient funds or payment failed"
            return False

        self.success = True
        self.log_transaction()
        return True
