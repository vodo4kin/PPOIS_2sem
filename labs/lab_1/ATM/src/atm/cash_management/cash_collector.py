from typing import Dict

from session_manager import logger as log
from ..config import Config


class CashCollector:
    """Handles cash collection (removal) from ATM cassettes by incassator."""

    def __init__(self, inventory) -> None:
        self.inventory = inventory
        self.logger = log.Logger()

    def collect(self, denominations: Dict[int, int]) -> None:
        """Remove cash from cassettes."""
        for denom, count in denominations.items():
            if denom in Config.ATM_CASH_DENOMINATIONS:
                if self.inventory._cassettes[denom] >= count:
                    self.inventory._cassettes[denom] -= count
                else:
                    raise ValueError(f"Not enough {denom} notes in cassette")
        self.inventory.save_state()
        self.logger.info(f"Cash collected: {denominations}")
