from .receipt_template import ReceiptTemplate
from session_manager import logger as log


class ReceiptPrinter:
    """Simulates printing receipts (console + optional file)."""

    def __init__(self) -> None:
        self.logger = log.Logger()

    def print_receipt(
        self,
        transaction_type: str,
        amount: float | None,
        balance_after: float | None,
        card_last4: str,
        success: bool,
        error: str | None = None
    ) -> None:
        receipt_text = ReceiptTemplate.generate(
            transaction_type, amount, balance_after, card_last4,
            success, error
        )
        print("\n" + receipt_text + "\n")
        self.logger.info("Receipt printed (simulated)")
        # Можно добавить запись в файл receipts.txt при желании
