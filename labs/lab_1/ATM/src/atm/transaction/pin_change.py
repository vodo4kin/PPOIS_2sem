from decimal import Decimal
from typing import TYPE_CHECKING

from .transaction import Transaction
from ..config import Config

if TYPE_CHECKING:
    from ..atm import ATM


class PinChangeTransaction(Transaction):
    """Transaction to change card PIN."""

    def __init__(self, atm: "ATM") -> None:
        super().__init__(atm, amount=None)

    def execute(self) -> bool:
        self.atm.display.show_message("Enter current PIN:")
        current_pin = self.atm.keypad.read_pin()

        card = self.atm.card_reader.get_current_card()
        if card is None:
            self.error_message = "No card"
            return False

        if not self.atm.bank_gateway.validate_pin(card.number, current_pin):
            self.error_message = "Current PIN incorrect"
            return False

        self.atm.display.show_message("Enter new PIN (4 digits):")
        new_pin = self.atm.keypad.read_pin()

        self.atm.display.show_message("Confirm new PIN:")
        confirm_pin = self.atm.keypad.read_pin()

        if new_pin != confirm_pin:
            self.error_message = "PINs do not match"
            return False

        from ..authentication.pin_validator import PinValidator
        if not PinValidator.is_valid_format(new_pin):
            self.error_message = "New PIN must be 4 digits"
            return False

        success = self.atm.bank_gateway.change_pin(card.number, new_pin)
        if success:
            self.atm.display.show_message("PIN changed successfully")
            self.success = True
            self.log_transaction()
            return True
        else:
            self.error_message = "PIN change failed (card blocked or not found)"
            return False
