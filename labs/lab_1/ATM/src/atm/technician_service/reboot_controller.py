from session_manager import logger as log
from power_controller import PowerController


class RebootController:
    """Handles ATM reboot."""

    def __init__(self, power_controller: PowerController) -> None:
        self.power_controller = power_controller
        self.logger = log.Logger()

    def reboot(self) -> None:
        self.power_controller.power_off()
        self.power_controller.power_on()
        self.logger.info("ATM rebooted")
