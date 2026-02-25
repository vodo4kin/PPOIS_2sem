"""Cash acceptor: accept deposited notes and update inventory."""

from ..config import Config
from ..session_manager.logger import Logger
from .cash_inventory import CashInventory


class CashAcceptor:
    """Simulates accepting cash deposits into the ATM."""

    def __init__(self, inventory: CashInventory) -> None:
        """Store reference to cash inventory."""
        self.inventory = inventory
        self.logger = Logger()

    def accept(self, denominations: dict[int, int]) -> int:
        """Accept cash as {denomination: count}; return total amount accepted."""
        total = 0
        for denom, count in denominations.items():
            if denom not in Config.ATM_CASH_DENOMINATIONS:
                raise ValueError(f"Unsupported denomination: {denom}")
            if count < 0:
                raise ValueError("Count cannot be negative")
            self.inventory._cassettes[denom] += count
            total += denom * count

        self.inventory.save_state()
        self.logger.info(
            f"Accepted cash: {total} BYN, breakdown: {denominations}")
        return total
