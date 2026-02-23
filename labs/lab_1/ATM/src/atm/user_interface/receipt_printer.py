"""Printing of receipts (checks) after client operations."""

from datetime import datetime
from typing import Any


class ReceiptPrinter:
    """Simulates printing a receipt (чек) after an operation."""

    def print_receipt(
        self,
        operation: str,
        success: bool,
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Output a receipt to the console (and optionally to file).
        operation: name of operation (e.g. "Check Balance", "Withdrawal")
        success: whether the operation succeeded
        message: result message to include
        kwargs: optional details (amount, balance, recipient, service, etc.)
        """
        lines = [
            "=" * 40,
            "                    RECEIPT / ЧЕК",
            "=" * 40,
            f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Operation: {operation}",
            f"Result: {'Success' if success else 'Failed'}",
            f"Details: {message}",
        ]
        for key, value in kwargs.items():
            if value is not None:
                lines.append(f"{key}: {value}")
        lines.append("=" * 40)
        text = "\n".join(lines)
        print(text)
        print()
