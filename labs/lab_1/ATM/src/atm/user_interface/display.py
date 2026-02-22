import os
from typing import List


class Display:
    """Simulates ATM screen output."""

    @staticmethod
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_message(self, message: str) -> None:
        self.clear()
        print("=" * 40)
        print(message.center(40))
        print("=" * 40)
        print()

    def show_menu(self, options: List[str]) -> str:
        self.clear()
        print("ATM Menu".center(40))
        print("-" * 40)
        for opt in options:
            print(opt)
        print("-" * 40)
        choice = input("Enter your choice: ").strip()
        return choice

    def show_menu_options_only(self, options: List[str]) -> None:  # pragma: no cover
        """Display menu options without reading choice (caller reads with timeout)."""
        self.clear()
        print("ATM Menu".center(40))
        print("-" * 40)
        for opt in options:
            print(opt)
        print("-" * 40)

    def ask_input(self, prompt: str) -> str:
        return input(prompt).strip()
