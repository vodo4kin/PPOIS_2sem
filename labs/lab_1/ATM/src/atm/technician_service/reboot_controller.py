from .power_controller import PowerController
from ..session_manager.logger import Logger


class RebootController:
    """Handles ATM reboot."""

    def __init__(self, power_controller: PowerController) -> None:
        self.power_controller = power_controller
        self.logger = Logger()

    def reboot(self) -> None:
        self.power_controller.power_off()
        self.power_controller.power_on()
        self.logger.info("ATM rebooted")
