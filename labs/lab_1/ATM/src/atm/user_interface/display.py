"""Display (screen) output simulation for the ATM."""

import os


class Display:
    """Simulates ATM screen output."""

    @staticmethod
    def clear() -> None:
        """Clear the screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_message(self, message: str) -> None:
        """Show a message centered on the screen."""
        self.clear()
        print("=" * 40)
        print(message.center(40))
        print("=" * 40)
        print()

    def show_menu(self, options: list[str]) -> str:
        """Display menu options and return user choice."""
        self.clear()
        print("ATM Menu".center(40))
        print("-" * 40)
        for opt in options:
            print(opt)
        print("-" * 40)
        choice = input("Enter your choice: ").strip()
        return choice

    def show_menu_options_only(self, options: list[str]) -> None:  # pragma: no cover
        """Display menu options without reading choice (caller reads with timeout)."""
        self.clear()
        print("ATM Menu".center(40))
        print("-" * 40)
        for opt in options:
            print(opt)
        print("-" * 40)

    def ask_input(self, prompt: str) -> str:
        """Prompt user and return trimmed input."""
        return input(prompt).strip()
