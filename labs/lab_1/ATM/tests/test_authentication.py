import pytest

from atm.authentication.pin_validator import PinValidator
from atm.authentication.card_block_status_checker import CardBlockStatusChecker
from atm.authentication.authentication_service import AuthenticationService
from atm.bank_communication.bank_gateway import BankGateway


class TestPinValidator:
    def test_valid_format(self):
        assert PinValidator.is_valid_format("1234") is True
        assert PinValidator.is_valid_format("0000") is True

    def test_invalid_format(self):
        assert PinValidator.is_valid_format("123") is False
        assert PinValidator.is_valid_format("12345") is False
        assert PinValidator.is_valid_format("12a4") is False


class TestCardBlockStatusChecker:
    def test_blocked_card(self):
        gw = BankGateway()
        checker = CardBlockStatusChecker(gw)
        assert checker.is_blocked("9999999999999999") is True

    def test_unblocked_card(self):
        gw = BankGateway()
        checker = CardBlockStatusChecker(gw)
        assert checker.is_blocked("1234") is False


class TestAuthenticationService:
    def test_authenticate_success(self):
        gw = BankGateway()
        auth = AuthenticationService(gw)
        assert auth.authenticate("1234567890123456", "0000") is True

    def test_authenticate_wrong_pin(self):
        gw = BankGateway()
        auth = AuthenticationService(gw)
        assert auth.authenticate("1234567890123456", "0001") is False

    def test_blocked_card_fails(self):
        gw = BankGateway()
        auth = AuthenticationService(gw)
        assert auth.authenticate("9999999999999999", "0000") is False

    def test_three_wrong_blocks_card(self):
        gw = BankGateway()
        auth = AuthenticationService(gw)
        auth.authenticate("1111111111111111", "0000")
        auth.authenticate("1111111111111111", "0000")
        auth.authenticate("1111111111111111", "0000")
        assert gw.is_card_blocked("1111111111111111") is True
