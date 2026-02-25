"""Simulates keypad input for the ATM."""


class Keypad:
    """Simulates keypad input."""

    def read_pin(self) -> str:
        """Read PIN from user (4 digits)."""
        pin = input("Enter PIN (4 digits): ").strip()
        return pin

    def read_input(self, prompt: str = "") -> str:
        """Read a line of input with optional prompt."""
        if prompt:
            print(prompt, end="")
        return input().strip()

    def read_amount(self) -> str:
        """Read amount from user."""
        return self.read_input("Enter amount: ")
