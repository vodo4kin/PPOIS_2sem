"""
Main ATM orchestrator module.
This class composes all subsystems and runs the main interaction loop.
"""

from typing import TYPE_CHECKING

from config import Config
from session_manager.logger import Logger
from session_manager.session import Session
from session_manager.atm_state_machine import ATMStateMachine, NoCardState
from bank_communication.bank_gateway import BankGateway
from card_reader.card_reader import CardReader
from authentication.authentication_service import AuthenticationService
from cash_handling.cash_inventory import CashInventory
from cash_handling.cash_dispenser import CashDispenser
from cash_handling.cash_acceptor import CashAcceptor
from user_interface.display import Display
from user_interface.keypad import Keypad
from user_interface.session_timer import SessionTimer

if TYPE_CHECKING:
    from .session_manager.state import State


class ATM:
    """
    Central class that orchestrates all ATM subsystems.

    Composes:
    - Logger
    - Bank gateway
    - Card reader & retainer
    - Authentication service
    - Session management & state machine
    - User interface (display, keypad)
    - Cash handling (inventory, dispenser, acceptor)
    - Session timer
    """

    # Type annotations for all major components (helps Pylance / mypy)
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

    def __init__(self) -> None:
        """Initialize all subsystems."""
        Config.ensure_data_dir()

        # Logging first — everything else will use it
        self.logger = Logger(log_file="atm.log")

        # Bank communication
        self.bank_gateway = BankGateway()

        # Card handling
        self.card_reader = CardReader()

        # Authentication
        self.auth_service = AuthenticationService(self.bank_gateway)

        # Session management
        self.session = Session()

        # User interface
        self.display = Display()
        self.keypad = Keypad()

        # Cash handling
        self.cash_inventory = CashInventory()
        self.cash_dispenser = CashDispenser(self.cash_inventory)
        self.cash_acceptor = CashAcceptor(self.cash_inventory)

        # Inactivity timer (callback will trigger session end)
        def on_timeout() -> None:
            self.display.show_message(Config.MSG_TIMEOUT)
            self.logger.warning("Session timed out due to inactivity")
            self.state_machine.change_state(
                SessionEndingState(self))  # type: ignore

        self.session_timer = SessionTimer(
            timeout_seconds=120, callback=on_timeout)

        # State machine — starts in NoCard state
        initial_state: State = NoCardState(self)
        self.state_machine = ATMStateMachine(self, initial_state)

        self.logger.info("ATM initialized successfully")

    def run(self) -> None:
        """Main ATM execution loop."""
        self.display.show_message(Config.MSG_WELCOME)
        self.logger.info("ATM main loop started")

        try:
            while True:
                # Reset timer after each interaction
                self.session_timer.reset()

                # Execute current state logic
                self.state_machine.handle()

                # Check for timeout (in case handle() didn't call reset)
                if self.session_timer.check_timeout():
                    self.logger.info("Timeout detected in main loop")

        except KeyboardInterrupt:
            self.display.show_message("Shutting down...")
            self.logger.info("ATM stopped by user (KeyboardInterrupt)")

        except Exception as e:
            self.logger.error(
                f"Critical error in main loop: {e}")
            self.display.show_message("System error. Please contact support.")

        finally:
            # Cleanup
            if self.session.is_active:
                self.session.end()
                self.card_reader.eject_card()
            self.logger.info("ATM session ended")
            self.logger.close()

    def reset_timer(self) -> None:
        """Convenience method to reset inactivity timer after user action."""
        self.session_timer.reset()
