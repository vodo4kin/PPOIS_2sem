"""
Main ATM orchestrator module.
Composes all subsystems and runs the main interaction loop.
"""

from typing import TYPE_CHECKING, Optional

from .config import Config
from .session_manager.logger import Logger
from .session_manager.session import Session
from .session_manager.atm_state_machine import (
    ATMStateMachine,
    NoCardState,
    SessionEndingState,
)
from .bank_communication.bank_gateway import BankGateway
from .card_reader.card_reader import CardReader
from .authentication.authentication_service import AuthenticationService
from .cash_handling.cash_inventory import CashInventory
from .cash_handling.cash_dispenser import CashDispenser
from .cash_handling.cash_acceptor import CashAcceptor
from .user_interface.display import Display
from .user_interface.keypad import Keypad
from .user_interface.session_timer import SessionTimer
from .user_interface.sound_player import SoundPlayer
from .cash_management.cash_replenisher_auth import CashReplenisherAuthenticator
from .cash_management.cash_replenisher import CashReplenisher
from .cash_management.cash_collector import CashCollector
from .cash_management.cassette_manager import CassetteManager
from .technician_service.technician_auth import TechnicianAuthenticator
from .technician_service.power_controller import PowerController
from .technician_service.reboot_controller import RebootController
from .technician_service.retained_card_collector import RetainedCardCollector
from .session_manager.session_type import SessionType

if TYPE_CHECKING:
    from .session_manager.state import State


class ATM:
    """Central orchestrator for all ATM subsystems."""

    logger: Logger
    bank_gateway: BankGateway
    card_reader: CardReader
    auth_service: AuthenticationService
    session: Session
    display: Display
    keypad: Keypad
    cash_inventory: CashInventory
    cash_dispenser: CashDispenser
    cash_acceptor: CashAcceptor
    state_machine: ATMStateMachine
    session_timer: SessionTimer
    cash_replenisher: CashReplenisher
    cash_collector: CashCollector
    cassette_manager: CassetteManager
    power_controller: PowerController
    reboot_controller: RebootController
    retained_card_collector: RetainedCardCollector
    sound_player: SoundPlayer

    def __init__(self) -> None:
        Config.ensure_data_dir()
        self.logger = Logger(log_file=str(Config.DATA_DIR / "atm.log"))
        self.bank_gateway = BankGateway()
        self.card_reader = CardReader()
        self.auth_service = AuthenticationService(self.bank_gateway)
        self.session = Session()
        self.display = Display()
        self.keypad = Keypad()
        self.cash_inventory = CashInventory()
        self.cash_dispenser = CashDispenser(self.cash_inventory)
        self.cash_acceptor = CashAcceptor(self.cash_inventory)
        self.state_machine = ATMStateMachine(self)

        def on_timeout() -> None:
            self.display.show_message(Config.MSG_TIMEOUT)
            self.logger.warning("Session timed out due to inactivity")
            if self.session.is_active and self.session.session_type == SessionType.CLIENT:
                self.state_machine.change_state(SessionEndingState(self.state_machine))
            elif self.session.is_active and self.session.session_type in (
                SessionType.CASH_REPLENISHER,
                SessionType.TECHNICIAN,
            ):
                self.session.end()

        self.session_timer = SessionTimer(
            timeout_seconds=Config.SESSION_TIMEOUT_SECONDS, callback=on_timeout
        )
        self.sound_player = SoundPlayer(self.logger)

        replenisher_auth = CashReplenisherAuthenticator(self.auth_service)
        self.cash_replenisher = CashReplenisher(
            self.cash_inventory, replenisher_auth)
        self.cash_collector = CashCollector(self.cash_inventory)
        self.cassette_manager = CassetteManager(self.cash_inventory)
        self.power_controller = PowerController()
        self.reboot_controller = RebootController(self.power_controller)
        self.retained_card_collector = RetainedCardCollector(
            self.card_reader.get_retainer())

        self.logger.info("ATM initialized successfully")

    def run(self) -> None:
        self.display.show_message(Config.MSG_WELCOME)
        self.logger.info("ATM main loop started")
        try:
            while True:
                self.session_timer.reset()
                choice = self.display.ask_input(
                    "Session type: 1 Client, 2 Incassator, 3 Technician, 4 Exit: "
                ).strip()
                self.session_timer.reset()
                if choice == "4":
                    break
                if choice == "1":
                    self._run_client_loop()
                elif choice == "2":
                    self._run_incassator_loop()
                elif choice == "3":
                    self._run_technician_loop()
                else:
                    self.display.show_message("Invalid choice.")
        except KeyboardInterrupt:
            self.display.show_message("Shutting down...")
            self.logger.info("ATM stopped by user (KeyboardInterrupt)")
        except Exception as e:
            self.logger.error(f"Critical error in main loop: {e}")
            self.display.show_message("System error. Please contact support.")
        finally:
            if self.session.is_active:
                self.session.end()
                self.card_reader.eject_card()
            self.logger.info("ATM session ended")
            self.logger.close()

    def _run_client_loop(self) -> None:
        try:
            while True:
                self.session_timer.reset()
                self.state_machine.handle()
                if self.session_timer.check_timeout():
                    self.logger.info("Timeout detected in main loop")
        except Exception as e:
            self.logger.error(f"Error in client loop: {e}")
            self.display.show_message(str(e))

    def _run_incassator_loop(self) -> None:
        card_id = self.keypad.read_input("Incassator card (16 digits, e.g. 1000000000000001): ").strip()
        pin = self.keypad.read_input("PIN: ").strip()
        if not self.auth_service.authenticate(card_id, pin):
            self.display.show_message("Authentication failed.")
            return
        self.session.start(SessionType.CASH_REPLENISHER, card_id)
        self.logger.info(f"Incassator session started: {card_id}")
        self.session_timer.reset()
        try:
            while True:
                action = self.keypad.read_input(
                    "1 Replenish, 2 Collect cash, 3 Replace cassette, 4 Exit: "
                ).strip()
                if self.session_timer.check_timeout():
                    break
                self.session_timer.reset()
                if action == "4":
                    break
                if action == "1":
                    inp = self.keypad.read_input(
                        "Denominations as 100:50 50:20 (denom:count): "
                    ).strip()
                    self.session_timer.reset()
                    try:
                        denoms = {}
                        for part in inp.split():
                            d, c = part.split(":")
                            denoms[int(d)] = int(c)
                        self.cash_replenisher.replenish(denoms, card_id, pin)
                        self.display.show_message("Replenished.")
                    except (ValueError, RuntimeError) as e:
                        self.display.show_message(f"Error: {e}")
                elif action == "2":
                    inp = self.keypad.read_input(
                        "Collect as 100:10 50:5: "
                    ).strip()
                    self.session_timer.reset()
                    try:
                        denoms = {}
                        for part in inp.split():
                            d, c = part.split(":")
                            denoms[int(d)] = int(c)
                        self.cash_collector.collect(denoms)
                        self.display.show_message("Collected.")
                    except (ValueError, RuntimeError) as e:
                        self.display.show_message(f"Error: {e}")
                elif action == "3":
                    d = self.keypad.read_input("Denomination to replace (e.g. 100): ").strip()
                    self.session_timer.reset()
                    c = self.keypad.read_input("New count: ").strip()
                    self.session_timer.reset()
                    try:
                        self.cassette_manager.replace_cassette(int(d), int(c))
                        self.display.show_message("Cassette replaced.")
                    except (ValueError, RuntimeError) as e:
                        self.display.show_message(f"Error: {e}")
        finally:
            self.session.end()

    def _run_technician_loop(self) -> None:
        card_id = self.keypad.read_input("Technician card (16 digits, e.g. 1000000000000002): ").strip()
        pin = self.keypad.read_input("PIN: ").strip()
        if not TechnicianAuthenticator(self.auth_service).authenticate(
            card_id, pin
        ):
            self.display.show_message("Authentication failed.")
            return
        self.session.start(SessionType.TECHNICIAN, card_id)
        self.logger.info(f"Technician session started: {card_id}")
        self.session_timer.reset()
        try:
            while True:
                action = self.keypad.read_input(
                    "1 Collect retained cards, 2 Reboot, 3 Exit: "
                ).strip()
                if self.session_timer.check_timeout():
                    break
                self.session_timer.reset()
                if action == "3":
                    break
                if action == "1":
                    cards = self.retained_card_collector.collect_retained()
                    self.display.show_message(
                        f"Collected {len(cards)} card(s): {cards}"
                    )
                elif action == "2":
                    self.reboot_controller.reboot()
                    self.display.show_message("Reboot completed.")
        finally:
            self.session.end()

    def reset_timer(self) -> None:
        self.session_timer.reset()

    def read_line_with_timeout(self, prompt: str) -> Optional[str]:
        """Read a line from user; returns None if inactivity timeout fired (session ended)."""
        from .user_interface.session_timer import read_line_with_timeout as _read
        return _read(prompt, self.session_timer)
