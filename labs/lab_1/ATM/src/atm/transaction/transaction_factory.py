from decimal import Decimal
from typing import TYPE_CHECKING, Dict, Any

from .transaction import Transaction
from .balance_inquiry import BalanceInquiryTransaction
from .withdrawal import WithdrawalTransaction
from .transfer import TransferTransaction
from .payment import PaymentTransaction

if TYPE_CHECKING:
    from ..atm import ATM


class TransactionFactory:
    """Factory for creating transaction instances."""

    @staticmethod
    def create(
        transaction_type: str,
        atm: "ATM",
        params: Dict[str, Any] | None = None
    ) -> Transaction:
        """Create appropriate transaction based on type."""
        params = params or {}

        if transaction_type == "balance":
            return BalanceInquiryTransaction(atm)

        elif transaction_type == "withdraw":
            amount = params.get("amount")
            if not isinstance(amount, (int, float, Decimal)):
                raise ValueError("Withdrawal requires valid amount")
            return WithdrawalTransaction(atm, Decimal(amount))

        elif transaction_type == "transfer":
            amount = params.get("amount")
            to_card = params.get("to_card", "")
            if not isinstance(amount, (int, float, Decimal)) or not to_card:
                raise ValueError("Transfer requires amount and to_card")
            return TransferTransaction(atm, Decimal(amount), to_card)

        elif transaction_type == "payment":
            amount = params.get("amount")
            service = params.get("service_name", "")
            if not isinstance(amount, (int, float, Decimal)):
                raise ValueError("Payment requires amount")
            return PaymentTransaction(atm, Decimal(amount), service)

        else:
            raise ValueError(f"Unknown transaction type: {transaction_type}")
