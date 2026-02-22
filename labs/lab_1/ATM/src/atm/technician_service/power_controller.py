from session_manager import logger as log


class PowerController:
    """Controls power on/off of ATM."""

    def __init__(self) -> None:
        self.is_on = True
        self.logger = log.Logger()

    def power_off(self) -> None:
        self.is_on = False
        self.logger.warning("ATM powered off")

    def power_on(self) -> None:
        self.is_on = True
        self.logger.info("ATM powered on")
