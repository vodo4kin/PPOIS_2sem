from typing import Dict, List, Optional
from dataclasses import asdict
from decimal import Decimal
import json
from pathlib import Path

from ..config import Config
from .account_data import AccountData


class MockBankRepository:
    """
    Simulated bank database using JSON file for persistence.
    All changes to accounts are saved to disk immediately.
    """

    def __init__(self) -> None:
        Config.ensure_data_dir()
        self.file_path: Path = Config.BANK_ACCOUNTS_FILE
        self._accounts = self._load_accounts()
        if not self._accounts:
            self._seed_demo_accounts()
            self._save_accounts()

    def _load_accounts(self) -> Dict[str, AccountData]:
        """
        Load accounts from JSON file.
        Returns empty dict if file not found or invalid.
        """
        if not self.file_path.exists():
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            accounts: Dict[str, AccountData] = {}
            for card_num, data in raw_data.items():
                try:
                    acc = AccountData(
                        card_number=data["card_number"],
                        pin_hash=data["pin_hash"],
                        balance=Decimal(data["balance"]),
                        is_blocked=data["is_blocked"],
                        is_retained=data.get("is_retained", False),
                        owner_name=data.get("owner_name"),
                        expiry_date=data.get("expiry_date"),
                    )
                    accounts[card_num] = acc
                except (ValueError, KeyError):
                    continue
            return accounts
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise RuntimeError(
                f"Failed to load bank accounts from {self.file_path}: {e}") from e
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error loading bank accounts: {e}") from e

    def _save_accounts(self) -> None:
        """
        Save current accounts to JSON file.
        Converts Decimal to str for JSON compatibility.
        """
        raw_data: Dict[str, dict] = {}
        for card_num, account in self._accounts.items():
            raw_data[card_num] = asdict(account)
            raw_data[card_num]["balance"] = str(raw_data[card_num]["balance"])
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(raw_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise RuntimeError(
                f"Failed to save bank accounts to {self.file_path}: {e}") from e

    def get_account(self, card_number: str) -> Optional[AccountData]:
        """
        Get account by card number.
        Returns None if card not found.
        """
        return self._accounts.get(card_number)

    def update_balance(self, card_number: str, new_balance: Decimal) -> bool:
        """
        Update account balance and save to disk.
        Returns True if successful, False if card not found or blocked.
        """
        account = self.get_account(card_number)
        if account is None or account.is_blocked:
            return False
        updated = AccountData(
            card_number=account.card_number,
            pin_hash=account.pin_hash,
            balance=new_balance,
            is_blocked=account.is_blocked,
            is_retained=account.is_retained,
            owner_name=account.owner_name,
            expiry_date=account.expiry_date,
        )
        self._accounts[card_number] = updated
        self._save_accounts()
        return True

    def block_card(self, card_number: str) -> bool:
        """
        Block the card and save to disk.
        Returns True if successful, False if card not found.
        """
        account = self.get_account(card_number)
        if account is None:
            return False
        updated = AccountData(
            card_number=account.card_number,
            pin_hash=account.pin_hash,
            balance=account.balance,
            is_blocked=True,
            is_retained=account.is_retained,
            owner_name=account.owner_name,
            expiry_date=account.expiry_date,
        )
        self._accounts[card_number] = updated
        self._save_accounts()
        return True

    def set_card_retained(self, card_number: str, retained: bool) -> bool:
        """Mark card as retained (seized by ATM) or not. Saves to disk."""
        account = self.get_account(card_number)
        if account is None:
            return False
        updated = AccountData(
            card_number=account.card_number,
            pin_hash=account.pin_hash,
            balance=account.balance,
            is_blocked=account.is_blocked,
            is_retained=retained,
            owner_name=account.owner_name,
            expiry_date=account.expiry_date,
        )
        self._accounts[card_number] = updated
        self._save_accounts()
        return True

    def get_retained_card_numbers(self) -> List[str]:
        """Return list of card numbers that are currently retained (in the machine)."""
        return [num for num, acc in self._accounts.items() if acc.is_retained]

    def collect_retained_cards(self, card_numbers: List[str]) -> None:
        """Mark cards as not retained and unblock. Used when technician collects."""
        for card_number in card_numbers:
            account = self.get_account(card_number)
            if account is None:
                continue
            updated = AccountData(
                card_number=account.card_number,
                pin_hash=account.pin_hash,
                balance=account.balance,
                is_blocked=False,
                is_retained=False,
                owner_name=account.owner_name,
                expiry_date=account.expiry_date,
            )
            self._accounts[card_number] = updated
        self._save_accounts()

    def validate_pin(self, card_number: str, pin: str) -> bool:
        """
        Validate PIN for the card.
        In simulation we compare plain string (in real life - hash verification).
        Returns True if PIN matches.
        """
        account = self.get_account(card_number)
        if account is None:
            return False
        return account.pin_hash == f"hashed_pin_{pin}"

    def add_account(self, account: AccountData) -> None:
        """
        Add or update account and save to disk.
        """
        self._accounts[account.card_number] = account
        self._save_accounts()

    def _seed_demo_accounts(self) -> None:
        """Create demo accounts when no bank_accounts.json exists. Card numbers are 16 digits."""
        expiry = "12/28"
        demos = [
            AccountData("1234567890123456", "hashed_pin_0000", Decimal("10000"), False, False, "Client One", expiry),
            AccountData("1111111111111111", "hashed_pin_1234", Decimal("5000"), False, False, "Client Two", expiry),
            AccountData("9999999999999999", "hashed_pin_0000", Decimal("0"), True, False, "Blocked Card", expiry),
            AccountData("1000000000000001", "hashed_pin_1111", Decimal("0"), False, False, "Incassator", expiry),
            AccountData("1000000000000002", "hashed_pin_2222", Decimal("0"), False, False, "Technician", expiry),
        ]
        for acc in demos:
            self._accounts[acc.card_number] = acc

    def get_all_accounts(self) -> Dict[str, AccountData]:
        """
        Return a copy of all accounts (for debugging or admin purposes).
        """
        return dict(self._accounts)

    def change_pin(self, card_number: str, new_pin: str) -> bool:
        """Change PIN hash for the card."""
        account = self.get_account(card_number)
        if account is None or account.is_blocked:
            return False
        new_hash = f"hashed_pin_{new_pin}"
        updated = AccountData(
            card_number=account.card_number,
            pin_hash=new_hash,
            balance=account.balance,
            is_blocked=account.is_blocked,
            is_retained=account.is_retained,
            owner_name=account.owner_name,
            expiry_date=account.expiry_date,
        )
        self._accounts[card_number] = updated
        self._save_accounts()
        return True

    def transfer(
        self, from_card: str, to_card: str, amount: Decimal
    ) -> bool:
        """Transfer amount from one card to another. Saves to disk."""
        from_acc = self.get_account(from_card)
        to_acc = self.get_account(to_card)
        if from_acc is None or to_acc is None or from_acc.is_blocked or to_acc.is_blocked:
            return False
        if from_acc.balance < amount or amount <= 0:
            return False
        self.update_balance(from_card, from_acc.balance - amount)
        self.update_balance(to_card, to_acc.balance + amount)
        return True
