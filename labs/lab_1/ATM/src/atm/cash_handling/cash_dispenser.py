from typing import Dict

from .cash_inventory import CashInventory
from session_manager import logger as log
from config import Config as conf


class CashDispenser:
    """Controls dispensing cash from cassettes."""

    def __init__(self, inventory: CashInventory) -> None:
        self.inventory = inventory
        self.logger = log.Logger()  # или передавать из ATM

    def dispense(self, amount: int) -> None:
        """Dispense the requested amount."""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        dispensed = self.inventory.dispense(amount)

        log_msg = f"Dispensed: {amount}. Breakdown: {dispensed}"
        self.logger.info(log_msg)

        # Здесь можно добавить симуляцию физической выдачи (print, sleep и т.д.)
        print("Dispensing cash...")
        for denom, count in dispensed.items():
            print(f"  {count} × {denom} {conf.DEFAULT_CURRENCY}")
