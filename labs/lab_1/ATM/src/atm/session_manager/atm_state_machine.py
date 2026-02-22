from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING

from ..config import Config
from .state import State
from .session import Session
from .session_type import SessionType
from .logger import Logger

if TYPE_CHECKING:
    from ..atm import ATM


class ATMStateMachine:
    """Finite State Machine that controls ATM behavior."""

    def __init__(self, atm: "ATM") -> None:
        self.atm: "ATM" = atm
        self.current_state: State = NoCardState(self)
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
            raise


def _normalize_card_number(raw: str) -> str:
    """Return card number as 16 digits or empty if invalid."""
    cleaned = raw.replace(" ", "").replace("-", "")
    if len(cleaned) != 16 or not cleaned.isdigit():
        return ""
    return cleaned


def _beep_and_wait(atm: "ATM", success: bool) -> None:
    """Beep (success or error) and wait for Enter."""
    if success:
        atm.sound_player.beep_success()
    else:
        atm.sound_player.beep_error()
    atm.keypad.read_input(Config.MSG_PRESS_ENTER)


class NoCardState(State):
    """Initial state — no card inserted."""

    def handle(self) -> None:
        card_number = _normalize_card_number(
            self.context.atm.display.ask_input(Config.MSG_INSERT_CARD)
        )
        if not card_number:
            self.context.atm.display.show_message(
                "Invalid card number. Must be exactly 16 digits.")
            return
        try:
            account = self.context.atm.bank_gateway.get_account(card_number)
            expiry = account.expiry_date if account else None
            card = self.context.atm.card_reader.insert_card(card_number, expiry)
            if card:
                self.context.atm.session.start(SessionType.CLIENT, card.number)
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

    def __init__(self, context: "ATMStateMachine") -> None:
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
    """User is authenticated — main menu with all operations."""

    def handle(self) -> None:
        from ..transaction.balance_inquiry import BalanceInquiryTransaction
        from ..transaction.deposit import DepositTransaction
        from ..transaction.transfer import TransferTransaction
        from ..transaction.payment import PaymentTransaction
        from ..transaction.pin_change import PinChangeTransaction

        options = [
            "1. Check Balance",
            "2. Withdraw",
            "3. Deposit",
            "4. Transfer",
            "5. Payment (services)",
            "6. Pin Change",
            "7. Exit",
        ]
        choice = self.context.atm.display.show_menu(options)
        atm = self.context.atm

        if choice == "1":
            t = BalanceInquiryTransaction(atm)
            ok = t.execute()
            if ok:
                atm.sound_player.beep_success()
            else:
                atm.display.show_message(t.get_result_message())
                atm.sound_player.beep_error()
            atm.keypad.read_input(Config.MSG_PRESS_ENTER)

        elif choice == "2":
            self.context.change_state(WithdrawalState(self.context))

        elif choice == "3":
            t = DepositTransaction(atm)
            ok = t.execute()
            if not ok and t.error_message:
                atm.display.show_message(t.get_result_message())
            _beep_and_wait(atm, ok)

        elif choice == "4":
            to_card = atm.keypad.read_input(
                "Enter recipient card number (16 digits): ").strip()
            amount_str = atm.keypad.read_input("Enter amount: ").strip()
            try:
                amount = Decimal(amount_str)
                t = TransferTransaction(atm, amount, to_card)
                ok = t.execute()
                msg = t.get_result_message()
                if not ok:
                    atm.display.show_message(msg)
                else:
                    atm.display.show_message("Transfer successful.")
                _beep_and_wait(atm, ok)
            except Exception:
                atm.display.show_message("Invalid amount.")
                _beep_and_wait(atm, False)

        elif choice == "5":
            service = atm.keypad.read_input("Enter service name: ").strip()
            amount_str = atm.keypad.read_input("Enter amount: ").strip()
            try:
                amount = Decimal(amount_str)
                t = PaymentTransaction(atm, amount, service)
                ok = t.execute()
                msg = t.get_result_message()
                if not ok:
                    atm.display.show_message(msg)
                else:
                    atm.display.show_message(
                        f"Payment successful. {service}: {amount} {Config.DEFAULT_CURRENCY}")
                _beep_and_wait(atm, ok)
            except Exception:
                atm.display.show_message("Invalid amount.")
                _beep_and_wait(atm, False)

        elif choice == "6":
            t = PinChangeTransaction(atm)
            ok = t.execute()
            if not ok and t.error_message:
                atm.display.show_message(t.get_result_message())
            _beep_and_wait(atm, ok)

        elif choice == "7":
            self.context.change_state(SessionEndingState(self.context))

        else:
            atm.display.show_message("Invalid choice.")
            atm.keypad.read_input(Config.MSG_PRESS_ENTER)


class WithdrawalState(State):
    """State for cash withdrawal."""

    def handle(self) -> None:
        amount_str = self.context.atm.keypad.read_input(
            "Enter amount (multiple of 100): ")
        atm = self.context.atm
        try:
            amount = int(amount_str)
            if amount % 100 != 0 or amount < Config.MIN_WITHDRAW_AMOUNT:
                raise ValueError(Config.MSG_INVALID_AMOUNT)
            success = atm.bank_gateway.withdraw(
                atm.card_reader.get_current_card().number,
                Decimal(amount)
            )
            if success:
                atm.cash_dispenser.dispense(amount)
                msg = f"Withdrawal successful. Take your {amount} {Config.DEFAULT_CURRENCY}"
                atm.display.show_message(msg)
                atm.sound_player.beep_success()
            else:
                atm.display.show_message(Config.MSG_INSUFFICIENT_FUNDS)
                atm.sound_player.beep_error()
        except ValueError as e:
            atm.display.show_message(str(e))
            atm.sound_player.beep_error()
        atm.keypad.read_input(Config.MSG_PRESS_ENTER)
        self.context.change_state(AuthenticatedState(self.context))


class SessionEndingState(State):
    """Ending session — eject card."""

    def handle(self) -> None:
        self.context.atm.display.show_message(Config.MSG_GOODBYE)
        self.context.atm.card_reader.eject_card()
        self.context.atm.session.end()
        self.context.change_state(NoCardState(self.context))
