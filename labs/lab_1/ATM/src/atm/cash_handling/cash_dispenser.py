from typing import Dict

from ..config import Config
from ..session_manager.logger import Logger
from .cash_inventory import CashInventory


class CashDispenser:
    """Controls dispensing cash from cassettes."""

    def __init__(self, inventory: CashInventory) -> None:
        self.inventory = inventory
        self.logger = Logger()

    def dispense(self, amount: int) -> None:
        """Dispense the requested amount."""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        dispensed = self.inventory.dispense(amount)

        log_msg = f"Dispensed: {amount}. Breakdown: {dispensed}"
        self.logger.info(log_msg)

        print("Dispensing cash...")
        for denom, count in dispensed.items():
            print(f"  {count} × {denom} {Config.DEFAULT_CURRENCY}")
