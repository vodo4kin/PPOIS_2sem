import json
from pathlib import Path
from typing import Any, Dict


class StateSaver:
    """Handles saving and loading ATM state to/from JSON."""

    def __init__(self, file_path: str | Path = "data/atm_state.json") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, state: Dict[str, Any]) -> None:
        """Save current state to file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to save state: {e}") from e

    def load(self) -> Dict[str, Any]:
        """Load state from file. Returns empty dict if file not found."""
        if not self.file_path.exists():
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in state file: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to load state: {e}") from e
