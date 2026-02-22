class Keypad:
    """Simulates keypad input."""

    def read_pin(self) -> str:
        pin = input("Enter PIN (4 digits): ").strip()
        return pin

    def read_input(self, prompt: str = "") -> str:
        if prompt:
            print(prompt, end="")
        return input().strip()

    def read_amount(self) -> str:
        return self.read_input("Enter amount: ")
