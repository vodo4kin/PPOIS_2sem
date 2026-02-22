from typing import TYPE_CHECKING

from ..session_manager.logger import Logger

if TYPE_CHECKING:
    from ..cash_handling.cash_inventory import CashInventory


class CassetteManager:
    """Manages physical cassettes in ATM."""

    def __init__(self, inventory: "CashInventory") -> None:
        self.inventory = inventory
        self.logger = Logger()

    def replace_cassette(self, denom: int, new_count: int) -> None:
        """Replace a cassette with new count."""
        if denom in self.inventory._cassettes:
            self.inventory._cassettes[denom] = new_count
            self.inventory.save_state()
            self.logger.info(
                f"Cassette {denom} replaced with {new_count} notes")
        else:
            raise ValueError("Unknown denomination")
