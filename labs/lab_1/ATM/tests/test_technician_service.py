from unittest.mock import MagicMock

import pytest

from atm.card_reader.card import Card
from atm.card_reader.card_retainer import CardRetainer
from atm.technician_service.power_controller import PowerController
from atm.technician_service.reboot_controller import RebootController
from atm.technician_service.retained_card_collector import RetainedCardCollector


class TestPowerController:
    def test_power_off_on(self):
        pc = PowerController()
        assert pc.is_on is True
        pc.power_off()
        assert pc.is_on is False
        pc.power_on()
        assert pc.is_on is True


class TestRebootController:
    def test_reboot(self):
        pc = PowerController()
        rc = RebootController(pc)
        rc.reboot()
        assert pc.is_on is True


class TestRetainedCardCollector:
    def test_collect_retained(self):
        r = CardRetainer()
        r.retain(Card(number="1234567890123456"))
        r.retain(Card(number="1111111111111111"))
        coll = RetainedCardCollector(r)
        cards = coll.collect_retained()
        assert set(cards) == {"1234567890123456", "1111111111111111"}
        assert len(r._retained) == 0
