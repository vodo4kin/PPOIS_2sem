from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class AccountData:
    """
    Data structure representing a bank account linked to a card.
    Immutable (frozen=True) to prevent accidental changes.
    """

    card_number: str
    """Card number, e.g. '1234-5678-9012-3456'."""

    pin_hash: str
    """Hashed PIN."""  # (in real life — bcrypt or argon2)

    balance: Decimal
    """Current account balance."""

    is_blocked: bool = False
    """True if card is blocked."""

    owner_name: Optional[str] = None
    """Optional: cardholder name."""

    def __post_init__(self) -> None:
        """Validate data after initialization."""
        if not self.card_number:
            raise ValueError("Card number cannot be empty")
        if self.balance < Decimal("0"):
            raise ValueError("Balance cannot be negative")
