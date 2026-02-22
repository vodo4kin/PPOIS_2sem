from atm.atm import ATM


def main() -> None:
    atm = ATM()
    try:
        atm.run()
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        print("ATM session ended.")


if __name__ == "__main__":
    main()
