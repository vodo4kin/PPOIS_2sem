from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from ..config import Config
from .state import State
from .session import Session
from .session_type import SessionType
from .logger import Logger
from decimal import Decimal

if TYPE_CHECKING:
    from ..atm import ATM


class ATMStateMachine:
    """Finite State Machine that controls ATM behavior."""

    def __init__(self, atm: "ATM", initial_state: State) -> None:
        self.atm: "ATM" = atm
        self.current_state: State = initial_state
        self.current_state.on_enter()
        self.logger: Logger = atm.logger

    def change_state(self, new_state: State) -> None:
        """Transition to a new state."""
        self.current_state.on_exit()
        self.current_state = new_state
        self.current_state.on_enter()
        self.logger.info(f"State changed to: {new_state.__class__.__name__}")

    def handle(self) -> None:
        """Execute logic of the current state."""
        try:
            self.current_state.handle()
        except Exception as e:
            self.logger.error(
                f"Error in state {self.current_state.__class__.__name__}: {e}")
            # Можно добавить переход в error state, если будет
            raise


# =============================================
# Конкретные состояния клиента (минимальный набор)
# =============================================


class NoCardState(State):
    """Initial state — no card inserted."""

    def handle(self) -> None:
        card_number = self.context.atm.display.ask_input(
            Config.MSG_INSERT_CARD)
        if card_number.strip():
            try:
                card = self.context.atm.card_reader.insert_card(
                    card_number.strip())
                if card:
                    self.context.atm.session.start(
                        SessionType.CLIENT, card.number)
                    self.context.change_state(CardInsertedState(self.context))
            except ValueError as e:
                self.context.atm.display.show_message(f"Error: {e}")
            except RuntimeError as e:
                self.context.atm.display.show_message(f"Error: {e}")


class CardInsertedState(State):
    """Card is inserted, waiting for PIN."""

    def handle(self) -> None:
        self.context.atm.display.show_message(
            "Card inserted. Please enter PIN.")
        self.context.change_state(EnteringPINState(self.context))


class EnteringPINState(State):
    """User is entering PIN code."""

    def __init__(self, context: "ATM") -> None:
        super().__init__(context)
        self.attempts: int = Config.MAX_PIN_ATTEMPTS

    def handle(self) -> None:
        pin = self.context.atm.keypad.read_pin()
        card_num = self.context.atm.card_reader.get_current_card().number

        if self.context.atm.auth_service.authenticate(card_num, pin):
            self.context.atm.display.show_message("Authentication successful!")
            self.context.change_state(AuthenticatedState(self.context))
        else:
            self.attempts -= 1
            if self.attempts <= 0:
                self.context.atm.display.show_message(Config.MSG_CARD_BLOCKED)
                self.context.atm.card_reader.retain_card()
                self.context.atm.session.end()
                self.context.change_state(NoCardState(self.context))
            else:
                msg = Config.MSG_INVALID_PIN.format(self.attempts)
                self.context.atm.display.show_message(msg)


class AuthenticatedState(State):
    """User is authenticated — main menu."""

    def handle(self) -> None:
        options = ["1. Check Balance", "2. Withdraw", "3. Exit"]
        choice = self.context.atm.display.show_menu(options)

        if choice == "1":
            balance = self.context.atm.bank_gateway.get_balance(
                self.context.atm.card_reader.get_current_card().number
            )
            if balance is not None:
                self.context.atm.display.show_message(
                    f"Your balance: {balance} {Config.DEFAULT_CURRENCY}")
            else:
                self.context.atm.display.show_message("Cannot get balance.")
        elif choice == "2":
            self.context.change_state(WithdrawalState(self.context))
        elif choice == "3":
            self.context.change_state(SessionEndingState(self.context))
        else:
            self.context.atm.display.show_message("Invalid choice.")


class WithdrawalState(State):
    """State for cash withdrawal."""

    def handle(self) -> None:
        amount_str = self.context.atm.keypad.read_input(
            "Enter amount (multiple of 100): ")
        try:
            amount = int(amount_str)
            if amount % 100 != 0 or amount < Config.MIN_WITHDRAW_AMOUNT:
                raise ValueError(Config.MSG_INVALID_AMOUNT)
            success = self.context.atm.bank_gateway.withdraw(
                self.context.atm.card_reader.get_current_card().number,
                Decimal(amount)
            )
            if success:
                self.context.atm.cash_dispenser.dispense(amount)
                self.context.atm.display.show_message(
                    f"Take your {amount} {Config.DEFAULT_CURRENCY}")
            else:
                self.context.atm.display.show_message(
                    Config.MSG_INSUFFICIENT_FUNDS)
        except ValueError as e:
            self.context.atm.display.show_message(str(e))
        finally:
            self.context.change_state(AuthenticatedState(self.context))


class SessionEndingState(State):
    """Ending session — eject card."""

    def handle(self) -> None:
        self.context.atm.display.show_message(Config.MSG_GOODBYE)
        self.context.atm.card_reader.eject_card()
        self.context.atm.session.end()
        self.context.change_state(NoCardState(self.context))
