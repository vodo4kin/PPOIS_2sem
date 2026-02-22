from typing import Optional
from ..config import Config as conf


class PinValidator:
    """Validates PIN format and correctness."""

    @staticmethod
    def is_valid_format(pin: str) -> bool:
        """Check if PIN is 4 digits."""
        return pin.isdigit() and len(pin) == conf.PIN_LENGTH

    @staticmethod
    def validate(
        entered_pin: str,
        expected_pin_hash: str  # in real system would be hashed
    ) -> bool:
        """Compare entered PIN with expected (simulated hash)."""
        # In real system: bcrypt.checkpw or similar
        simulated_hash = f"hashed_{entered_pin}"
        return simulated_hash == expected_pin_hash
