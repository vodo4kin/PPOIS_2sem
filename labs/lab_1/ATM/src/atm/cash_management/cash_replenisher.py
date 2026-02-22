from typing import Dict

from .cash_replenisher_auth import CashReplenisherAuthenticator
from session_manager import logger as log
from ..config import Config


class CashReplenisher:
    """Handles cash replenishment by incassator."""

    def __init__(self, inventory, authenticator: CashReplenisherAuthenticator) -> None:
        self.inventory = inventory
        self.authenticator = authenticator
        self.logger = log.Logger()

    def replenish(self, denominations: Dict[int, int], user_id: str, pin: str) -> None:
        """Replenish with authentication."""
        if not self.authenticator.authenticate(user_id, pin):
            raise RuntimeError("Authentication failed for replenisher")
        for denom, count in denominations.items():
            if denom in Config.ATM_CASH_DENOMINATIONS:
                self.inventory._cassettes[denom] += count
        self.inventory.save_state()
        self.logger.info(f"Cash replenished by {user_id}: {denominations}")
