from datetime import datetime
from typing import Dict, Any


class ReceiptTemplate:
    """Template for generating receipt text."""

    @staticmethod
    def generate(
        transaction_type: str,
        amount: float | None,
        balance_after: float | None,
        card_last4: str,
        success: bool,
        error: str | None = None
    ) -> str:
        lines = [
            "=== ATM Receipt ===",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Card: **** **** **** {card_last4}",
            f"Transaction: {transaction_type}",
        ]

        if amount is not None:
            lines.append(f"Amount: {amount:.2f} BYN")

        if balance_after is not None:
            lines.append(f"New balance: {balance_after:.2f} BYN")

        if success:
            lines.append("Status: SUCCESS")
        else:
            lines.append(f"Status: FAILED - {error or 'Unknown error'}")

        lines.extend([
            "-" * 30,
            "Thank you for using our ATM",
            "=== End of Receipt ==="
        ])

        return "\n".join(lines)
