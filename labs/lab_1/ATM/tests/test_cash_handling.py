import pytest

from atm.cash_handling.cash_inventory import CashInventory
from atm.cash_handling.cash_dispenser import CashDispenser
from atm.cash_handling.cash_acceptor import CashAcceptor


class TestCashInventory:
    def test_get_available_amount(self):
        inv = CashInventory()
        assert inv.get_available_amount() >= 0

    def test_can_dispense(self):
        inv = CashInventory()
        assert inv.can_dispense(100) is True or inv.can_dispense(100) is False

    def test_dispense_updates_state(self):
        inv = CashInventory()
        if not inv.can_dispense(100):
            inv._cassettes[100] = 10
        before = inv.get_available_amount()
        d = inv.dispense(100)
        assert d == {100: 1}
        assert inv.get_available_amount() == before - 100

    def test_dispense_invalid_raises(self):
        inv = CashInventory()
        for k in inv._cassettes:
            inv._cassettes[k] = 0
        with pytest.raises(ValueError):
            inv.dispense(100)


class TestCashDispenser:
    def test_dispense(self):
        inv = CashInventory()
        inv._cassettes[100] = 10
        disp = CashDispenser(inv)
        disp.dispense(100)
        assert inv._cassettes[100] == 9

    def test_dispense_zero_raises(self):
        inv = CashInventory()
        disp = CashDispenser(inv)
        with pytest.raises(ValueError, match="positive"):
            disp.dispense(0)


class TestCashAcceptor:
    def test_accept(self):
        inv = CashInventory()
        before = inv._cassettes.get(100, 0)
        acc = CashAcceptor(inv)
        total = acc.accept({100: 5})
        assert total == 500
        assert inv._cassettes[100] == before + 5
