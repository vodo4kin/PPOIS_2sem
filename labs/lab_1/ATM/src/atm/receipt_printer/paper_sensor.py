from typing import Optional
from session_manager import logger as log
from ..config import Config


class PaperSensor:
    """
    Simulates paper sensor in the receipt printer module.

    Detects presence/absence of receipt paper roll and tracks remaining length.
    In real hardware this would interface with physical sensors.
    """

    def __init__(self, initial_length_mm: int = 50000) -> None:
        """
        Initialize paper sensor.

        Args:
            initial_length_mm: Initial length of paper roll in millimeters (default: 50 meters).
        """
        if initial_length_mm <= 0:
            raise ValueError("Initial paper length must be positive")

        self._remaining_length_mm: int = initial_length_mm
        self._min_safe_length_mm: int = 5000  # ~5 meters remaining → warning
        self._critical_length_mm: int = 1000  # ~1 meter remaining → error
        self.logger: log.Logger = log.Logger()  # Можно передать извне, если нужно

    def has_paper(self) -> bool:
        """Check if there is any paper left in the printer."""
        return self._remaining_length_mm > 0

    def is_low(self) -> bool:
        """Check if paper level is low (warning threshold)."""
        return self._remaining_length_mm <= self._min_safe_length_mm

    def is_critical(self) -> bool:
        """Check if paper is critically low (cannot print safely)."""
        return self._remaining_length_mm <= self._critical_length_mm

    def consume(self, length_mm: int) -> None:
        """
        Consume specified length of paper during printing.

        Raises:
            RuntimeError: If attempting to print without enough paper.
        """
        if length_mm <= 0:
            raise ValueError("Length to consume must be positive")

        if self._remaining_length_mm < length_mm:
            self.logger.error(
                f"Out of paper: need {length_mm} mm, available {self._remaining_length_mm} mm"
            )
            raise RuntimeError("Out of receipt paper. Please contact service.")

        self._remaining_length_mm -= length_mm
        self.logger.info(
            f"Consumed {length_mm} mm of paper. Remaining: {self._remaining_length_mm} mm")

        if self.is_critical():
            self.logger.warning(
                "Paper critically low — urgent replacement needed")
        elif self.is_low():
            self.logger.warning("Paper low — consider replacing soon")

    def get_remaining_mm(self) -> int:
        """Get current remaining paper length in millimeters."""
        return self._remaining_length_mm

    def get_status_message(self) -> str:
        """Get human-readable status for display."""
        remaining = self._remaining_length_mm / 1000  # в метрах для удобства
        if not self.has_paper():
            return "NO PAPER - Printer offline"
        if self.is_critical():
            return f"CRITICAL LOW PAPER ({remaining:.1f} m left)"
        if self.is_low():
            return f"LOW PAPER ({remaining:.1f} m left)"
        return f"Paper OK ({remaining:.1f} m remaining)"

    def refill(self, added_length_mm: int) -> None:
        """Refill paper roll (used by technician or service)."""
        if added_length_mm <= 0:
            raise ValueError("Added length must be positive")

        self._remaining_length_mm += added_length_mm
        self.logger.info(
            f"Paper refilled by {added_length_mm} mm. New total: {self._remaining_length_mm} mm")
