from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from ..config import Config

if TYPE_CHECKING:
    from ..atm import ATM


class Transaction(ABC):
    """Abstract base class for all ATM transactions."""

    def __init__(self, atm: "ATM", amount: Decimal | None = None) -> None:
        self.atm = atm
        self.amount = amount
        self.success: bool = False
        self.error_message: str | None = None

    @abstractmethod
    def execute(self) -> bool:
        """Execute the transaction logic."""
        pass

    def get_result_message(self) -> str:
        """Get human-readable result for display."""
        if self.success:
            return "Transaction successful."
        return self.error_message or "Transaction failed."

    def log_transaction(self) -> None:
        """Log transaction result."""
        status = "SUCCESS" if self.success else "FAILED"
        msg = f"{self.__class__.__name__} - {status}"
        if self.amount is not None:
            msg += f" amount={self.amount}"
        if self.error_message:
            msg += f" error={self.error_message}"
        self.atm.logger.info(msg)
