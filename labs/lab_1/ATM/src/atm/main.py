"""Entry point for the ATM application."""

from atm.atm import ATM


def main() -> None:
    """Create ATM, run main loop, handle shutdown."""
    atm = ATM()
    try:
        atm.run()
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        print("ATM session ended.")


if __name__ == "__main__":
    main()
