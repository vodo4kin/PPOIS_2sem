import json
from typing import Any, Dict
from ..config import Config


class StateSaver:
    """Handles saving and loading ATM state to/from JSON."""

    def __init__(self) -> None:
        Config.ensure_data_dir()
        self.file_path = Config.ATM_STATE_FILE

    def save(self, state: Dict[str, Any]) -> None:
        """Save current state to file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise RuntimeError(
                f"Failed to save state to {self.file_path}: {e}") from e

    def load(self) -> Dict[str, Any]:
        """Load state from file. Returns empty dict if file not found."""
        if not self.file_path.exists():
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in {self.file_path}: {e}") from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to load state from {self.file_path}: {e}") from e
