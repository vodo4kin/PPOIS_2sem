from pathlib import Path
from typing import Final, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Config:
    """Global configuration constants for the ATM system."""

    DATA_DIR: Final[Path] = _PROJECT_ROOT / "data"
    ATM_STATE_FILE: Final[Path] = DATA_DIR / "atm_state.json"
    BANK_ACCOUNTS_FILE: Final[Path] = DATA_DIR / "bank_accounts.json"
    MAX_PIN_ATTEMPTS: Final[int] = 3
    PIN_LENGTH: Final[int] = 4
    MIN_WITHDRAW_AMOUNT: Final[int] = 100
    MAX_WITHDRAW_AMOUNT_PER_DAY: Final[int] = 50000
    SESSION_TIMEOUT_SECONDS: Final[int] = 60
    """Inactivity timeout: session ends after this many seconds without user input."""
    DEFAULT_CURRENCY: Final[str] = "BYN"
    ATM_CASH_DENOMINATIONS: Final[Tuple[int, ...]] = (
        20, 50, 100, 200, 500, 1000)
    MSG_WELCOME: Final[str] = "Welcome to the ATM"
    MSG_INSERT_CARD: Final[str] = "Enter card number (16 digits): "
    MSG_ENTER_PIN: Final[str] = "Enter PIN: "
    MSG_INVALID_PIN: Final[str] = "Invalid PIN. Attempts left: {}"
    MSG_CARD_BLOCKED: Final[str] = "Card is blocked. Contact your bank."
    MSG_GOODBYE: Final[str] = "Thank you. Please take your card."
    MSG_TIMEOUT: Final[str] = "Session timed out due to inactivity."
    MSG_INSUFFICIENT_FUNDS: Final[str] = "Insufficient funds."
    MSG_INVALID_AMOUNT: Final[str] = "Invalid amount. Must be multiple of 100."
    MSG_PRESS_ENTER: Final[str] = "Press Enter to continue..."

    @classmethod
    def ensure_data_dir(cls) -> None:
        """Create data directory if it does not exist."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
