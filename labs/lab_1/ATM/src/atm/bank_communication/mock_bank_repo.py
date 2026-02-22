from typing import Dict, Optional
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
        Config.ensure_data_dir()  # создаём папку data/, если её нет
        self.file_path: Path = Config.BANK_ACCOUNTS_FILE
        self._accounts: Dict[str, AccountData] = self._load_accounts()

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
                accounts[card_num] = AccountData(
                    card_number=data["card_number"],
                    pin_hash=data["pin_hash"],
                    balance=Decimal(data["balance"]),
                    is_blocked=data["is_blocked"],
                    owner_name=data.get("owner_name")
                )
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
            raw_data[card_num]["balance"] = str(
                raw_data[card_num]["balance"])  # Decimal → str
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
            owner_name=account.owner_name
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
            owner_name=account.owner_name
        )
        self._accounts[card_number] = updated
        self._save_accounts()
        return True

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
            owner_name=account.owner_name
        )
        self._accounts[card_number] = updated
        self._save_accounts()
        return True
