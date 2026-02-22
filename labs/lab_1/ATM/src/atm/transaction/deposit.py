from decimal import Decimal
from typing import TYPE_CHECKING, Dict

from ..cash_handling import cash_acceptor
from .transaction import Transaction
from ..config import Config
from ..atm import ATM


class DepositTransaction(Transaction):
    """Transaction for depositing cash."""

    def __init__(self, atm: "ATM") -> None:
        super().__init__(atm, amount=None)

    def execute(self) -> bool:
        self.atm.display.show_message("Please insert cash into acceptor.")
        # Симуляция ввода купюр пользователем (в реальности — аппаратный ввод)
        try:
            input_str = self.atm.keypad.read_input(
                "Enter denominations as '100:3 50:2' or empty to cancel: "
            )
            if not input_str.strip():
                self.error_message = "Deposit cancelled"
                return False

            denominations: Dict[int, int] = {}
            for part in input_str.split():
                denom_str, count_str = part.split(":")
                denom = int(denom_str)
                count = int(count_str)
                denominations[denom] = count

            accepted = self.atm.cash_acceptor.accept(denominations)
            if accepted <= 0:
                raise ValueError("No cash accepted")

            card = self.atm.card_reader.get_current_card()
            if card is None:
                raise RuntimeError("No card during deposit")

            success = self.atm.bank_gateway.deposit(
                card.number, Decimal(accepted))
            if success:
                self.atm.display.show_message(
                    f"Deposited {accepted} {Config.DEFAULT_CURRENCY}")
                self.success = True
                self.log_transaction()
                return True
            else:
                # Откат (возвращаем купюры пользователю — симуляция)
                self.atm.display.show_message("Deposit failed. Cash returned.")
                return False

        except (ValueError, KeyError) as e:
            self.error_message = f"Invalid input: {e}"
            return False
        except RuntimeError as e:
            self.error_message = str(e)
            return False
