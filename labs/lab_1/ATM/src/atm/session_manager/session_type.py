from enum import Enum, auto


class SessionType(Enum):
    """Type of the current ATM session."""

    CLIENT = auto()
    CASH_REPLENISHER = auto()
    TECHNICIAN = auto()
