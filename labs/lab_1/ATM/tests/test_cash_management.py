from unittest.mock import MagicMock

import pytest

from atm.cash_handling.cash_inventory import CashInventory
from atm.cash_management.cash_replenisher import CashReplenisher
from atm.cash_management.cash_collector import CashCollector
from atm.cash_management.cassette_manager import CassetteManager
from atm.cash_management.cash_replenisher_auth import CashReplenisherAuthenticator


class TestCashReplenisher:
    def test_replenish_requires_auth(self):
        auth_svc = MagicMock()
        auth_svc.authenticate.return_value = False
        auth = CashReplenisherAuthenticator(auth_svc)
        inv = CashInventory()
        rep = CashReplenisher(inv, auth)
        with pytest.raises(RuntimeError, match="Authentication failed"):
            rep.replenish({100: 10}, "1000000000000001", "wrong")

    def test_replenish_success(self):
        auth_svc = MagicMock()
        auth_svc.authenticate.return_value = True
        auth = CashReplenisherAuthenticator(auth_svc)
        inv = CashInventory()
        rep = CashReplenisher(inv, auth)
        rep.replenish({100: 10}, "1000000000000001", "1111")
        assert inv._cassettes[100] >= 10


class TestCashCollector:
    def test_collect(self):
        inv = CashInventory()
        inv._cassettes[100] = 20
        coll = CashCollector(inv)
        coll.collect({100: 5})
        assert inv._cassettes[100] == 15


class TestCassetteManager:
    def test_replace_cassette(self):
        inv = CashInventory()
        mgr = CassetteManager(inv)
        mgr.replace_cassette(100, 99)
        assert inv._cassettes[100] == 99
