import json
from pathlib import Path
from typing import Dict

from ..config import Config
from ..session_manager.state_saver import StateSaver


class CashInventory:
    """Manages cash denominations inside the ATM."""

    def __init__(self) -> None:
        self._cassettes: Dict[int, int] = {
            denom: 50 for denom in Config.ATM_CASH_DENOMINATIONS}
        self._saver = StateSaver()
        self._load_state()

    def _load_state(self) -> None:
        """Load cash inventory from persistent storage."""
        state = self._saver.load()
        cash_state = state.get("cash_inventory", {})
        for denom_str, count in cash_state.items():
            try:
                denom = int(denom_str)
                if denom in self._cassettes:
                    self._cassettes[denom] = max(0, count)
            except ValueError:
                pass

    def save_state(self) -> None:
        """Save current cash state."""
        state = self._saver.load()
        state["cash_inventory"] = {
            str(k): v for k, v in self._cassettes.items()}
        self._saver.save(state)

    def get_available_amount(self) -> int:
        """Total cash available in ATM."""
        return sum(denom * count for denom, count in self._cassettes.items())

    def can_dispense(self, amount: int) -> bool:
        """Check if we can dispense exact amount with available denominations."""
        if amount % 100 != 0:
            return False
        remaining = amount
        for denom in sorted(self._cassettes.keys(), reverse=True):
            if denom > remaining:
                continue
            count_needed = remaining // denom
            if count_needed <= self._cassettes[denom]:
                remaining -= count_needed * denom
            else:
                remaining -= self._cassettes[denom] * denom
        return remaining == 0

    def dispense(self, amount: int) -> Dict[int, int]:
        """Dispense cash and update inventory."""
        if not self.can_dispense(amount):
            raise ValueError(
                "Cannot dispense requested amount with available notes")

        dispensed: Dict[int, int] = {}
        remaining = amount
        for denom in sorted(self._cassettes.keys(), reverse=True):
            if denom > remaining:
                continue
            count = min(remaining // denom, self._cassettes[denom])
            if count > 0:
                dispensed[denom] = count
                self._cassettes[denom] -= count
                remaining -= count * denom

        if remaining != 0:
            raise RuntimeError("Dispense logic error")

        self.save_state()
        return dispensed
