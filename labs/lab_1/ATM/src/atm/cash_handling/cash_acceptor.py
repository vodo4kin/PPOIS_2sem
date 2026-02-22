from typing import Dict

from ..config import Config
from .cash_inventory import CashInventory
from session_manager import logger


class CashAcceptor:
    """Simulates accepting cash deposits into the ATM."""

    def __init__(self, inventory: CashInventory) -> None:
        self.inventory = inventory
        self.logger = logger.Logger()

    def accept(self, denominations: Dict[int, int]) -> int:
        """
        Accept cash in form of {denomination: count}.
        Returns total accepted amount or raises exception on error.
        """
        total = 0
        for denom, count in denominations.items():
            if denom not in Config.ATM_CASH_DENOMINATIONS:
                raise ValueError(f"Unsupported denomination: {denom}")
            if count < 0:
                raise ValueError("Count cannot be negative")
            # прямой доступ (в реальности — метод add)
            self.inventory._cassettes[denom] += count
            total += denom * count

        self.inventory.save_state()
        self.logger.info(
            f"Accepted cash: {total} BYN, breakdown: {denominations}")
        return total
