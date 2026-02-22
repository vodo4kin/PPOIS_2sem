import pytest

from atm.card_reader.card_reader import CardReader


class TestCardReader:
    def test_insert_and_get_current(self):
        r = CardReader()
        assert r.get_current_card() is None
        card = r.insert_card("1234567890123456")
        assert card is not None
        assert r.get_current_card().number == "1234567890123456"

    def test_eject_card(self):
        r = CardReader()
        r.insert_card("1234567890123456")
        r.eject_card()
        assert r.get_current_card() is None

    def test_retain_card(self):
        r = CardReader()
        r.insert_card("1234567890123456")
        r.retain_card()
        assert r.get_current_card() is None
        assert len(r.get_retainer()._retained) == 1
        assert r.get_retainer()._retained[0].number == "1234567890123456"

    def test_double_insert_raises(self):
        r = CardReader()
        r.insert_card("1234567890123456")
        with pytest.raises(RuntimeError, match="already inserted"):
            r.insert_card("1111111111111111")
