"""ATM reboot: power off then on."""

from .power_controller import PowerController
from ..session_manager.logger import Logger


class RebootController:
    """Handles ATM reboot."""

    def __init__(self, power_controller: PowerController) -> None:
        """Store reference to power controller."""
        self.power_controller = power_controller
        self.logger = Logger()

    def reboot(self) -> None:
        """Perform power off then power on."""
        self.power_controller.power_off()
        self.power_controller.power_on()
        self.logger.info("ATM rebooted")
