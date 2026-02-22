import datetime
from typing import Optional


class Logger:
    """Simple logger for ATM events."""

    def __init__(self, log_file: Optional[str] = None) -> None:
        self.log_file = log_file
        self._file_handle = None
        if self.log_file:
            self._file_handle = open(self.log_file, "a", encoding="utf-8")

    def info(self, message: str) -> None:
        self._log("INFO", message)

    def warning(self, message: str) -> None:
        self._log("WARNING", message)

    def error(self, message: str) -> None:
        self._log("ERROR", message)

    def _log(self, level: str, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {level:8} {message}"
        print(log_line)
        if self._file_handle:
            print(log_line, file=self._file_handle, flush=True)

    def close(self) -> None:
        """Close log file if opened."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
