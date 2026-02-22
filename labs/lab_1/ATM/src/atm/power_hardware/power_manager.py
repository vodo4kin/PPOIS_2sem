from session_manager import logger as log


class PowerManager:
    """Manages power and hardware status."""

    def __init__(self) -> None:
        self.is_powered = True
        self.logger = log.Logger()

    def shutdown(self) -> None:
        self.is_powered = False
        self.logger.warning("Power shutdown initiated")

    def startup(self) -> None:
        self.is_powered = True
        self.logger.info("Power startup completed")
