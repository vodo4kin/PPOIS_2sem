from typing import TYPE_CHECKING

from ..config import Config
from .transaction import Transaction

if TYPE_CHECKING:
    from ..atm import ATM


class BalanceInquiryTransaction(Transaction):
    """Transaction to check account balance."""

    def __init__(self, atm: "ATM") -> None:
        super().__init__(atm, amount=None)

    def execute(self) -> bool:
        card = self.atm.card_reader.get_current_card()
        if card is None:
            self.error_message = "No card inserted"
            return False

        balance = self.atm.bank_gateway.get_balance(card.number)
        if balance is None:
            self.error_message = "Cannot retrieve balance"
            return False

        self.atm.display.show_message(
            f"Current balance: {balance} {Config.DEFAULT_CURRENCY}")
        self.success = True
        self.log_transaction()
        return True
