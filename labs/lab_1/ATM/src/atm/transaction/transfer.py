from decimal import Decimal
from typing import TYPE_CHECKING

from .transaction import Transaction
from ..config import Config

if TYPE_CHECKING:
    from ..atm import ATM


class TransferTransaction(Transaction):
    """Transaction for transferring funds to another card."""

    def __init__(
        self, atm: "ATM", amount: Decimal, to_card_number: str
    ) -> None:
        super().__init__(atm, amount=amount)
        self.to_card_number = to_card_number

    def execute(self) -> bool:
        if self.amount is None or self.amount <= 0:
            self.error_message = "Amount must be positive"
            return False

        card = self.atm.card_reader.get_current_card()
        if card is None:
            self.error_message = "No card inserted"
            return False

        from_card = card.number
        to_card = self.to_card_number.replace(" ", "").replace("-", "")
        if len(to_card) != 16 or not to_card.isdigit():
            self.error_message = "Recipient card number must be 16 digits"
            return False

        if not self.atm.bank_gateway.transfer(from_card, to_card, self.amount):
            self.error_message = "Transfer failed (insufficient funds or invalid recipient)"
            return False

        self.success = True
        self.log_transaction()
        return True
