from pathlib import Path
from typing import Final, Tuple


class Config:
    """Global configuration constants for the ATM system."""

    # Paths
    DATA_DIR: Final[Path] = Path("data")
    ATM_STATE_FILE: Final[Path] = DATA_DIR / "atm_state.json"
    BANK_ACCOUNTS_FILE: Final[Path] = DATA_DIR / "bank_accounts.json"

    # Limits and rules
    MAX_PIN_ATTEMPTS: Final[int] = 3
    PIN_LENGTH: Final[int] = 4
    MIN_WITHDRAW_AMOUNT: Final[int] = 100
    MAX_WITHDRAW_AMOUNT_PER_DAY: Final[int] = 50000
    DEFAULT_CURRENCY: Final[str] = "BYN"

    # Cash denominations available in the ATM cassettes (in BYN)
    ATM_CASH_DENOMINATIONS: Final[Tuple[int, ...]] = (
        20, 50, 100, 200, 500, 1000)

    # Messages (English only)
    MSG_WELCOME: Final[str] = "Welcome to the ATM"
    MSG_INSERT_CARD: Final[str] = "Please insert your card (enter card number): "
    MSG_ENTER_PIN: Final[str] = "Enter PIN: "
    MSG_INVALID_PIN: Final[str] = "Invalid PIN. Attempts left: {}"
    MSG_CARD_BLOCKED: Final[str] = "Card is blocked. Contact your bank."
    MSG_GOODBYE: Final[str] = "Thank you. Please take your card."
    MSG_TIMEOUT: Final[str] = "Session timed out due to inactivity."
    MSG_INSUFFICIENT_FUNDS: Final[str] = "Insufficient funds."
    MSG_INVALID_AMOUNT: Final[str] = "Invalid amount. Must be multiple of 100."

    @classmethod
    def ensure_data_dir(cls) -> None:
        """Create data directory if it does not exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
