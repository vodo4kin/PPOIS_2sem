from typing import Dict, TYPE_CHECKING

from ..config import Config
from ..session_manager.logger import Logger
from .cash_replenisher_auth import CashReplenisherAuthenticator

if TYPE_CHECKING:
    from ..cash_handling.cash_inventory import CashInventory


class CashReplenisher:
    """Handles cash replenishment by incassator."""

    def __init__(
        self,
        inventory: "CashInventory",
        authenticator: CashReplenisherAuthenticator,
    ) -> None:
        self.inventory = inventory
        self.authenticator = authenticator
        self.logger = Logger()

    def replenish(self, denominations: Dict[int, int], user_id: str, pin: str) -> None:
        """Replenish with authentication."""
        if not self.authenticator.authenticate(user_id, pin):
            raise RuntimeError("Authentication failed for replenisher")
        for denom, count in denominations.items():
            if denom in Config.ATM_CASH_DENOMINATIONS:
                self.inventory._cassettes[denom] += count
        self.inventory.save_state()
        self.logger.info(f"Cash replenished by {user_id}: {denominations}")
