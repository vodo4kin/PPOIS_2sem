from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Card:
    """Immutable representation of a bank card."""

    number: str
    owner: Optional[str] = None
    expiry_date: Optional[str] = None

    def __post_init__(self) -> None:
        cleaned = self.number.replace("-", "").replace(" ", "")
        if len(cleaned) != 16 or not cleaned.isdigit():
            raise ValueError("Card number must be exactly 16 digits")
