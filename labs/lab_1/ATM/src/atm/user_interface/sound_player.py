from ..session_manager.logger import Logger


class SoundPlayer:
    """Plays sound feedback (simulated via log). Beep on success or error."""

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def beep_success(self) -> None:
        """Signal successful operation."""
        self._logger.info("*Beep*")

    def beep_error(self) -> None:
        """Signal error."""
        self._logger.error("*Beep*")
