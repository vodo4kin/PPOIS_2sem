from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Card:
    """Immutable representation of a bank card."""

    number: str
    owner: Optional[str] = None
    expiry_date: Optional[str] = None  # format: MM/YY

    def __post_init__(self) -> None:
        if not self.number or len(self.number.replace("-", "")) != 16:
            raise ValueError("Invalid card number format")
