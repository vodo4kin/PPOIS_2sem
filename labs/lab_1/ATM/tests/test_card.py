import pytest

from atm.card_reader.card import Card


class TestCard:
    def test_create_valid(self):
        c = Card(number="1234567890123456")
        assert c.number == "1234567890123456"

    def test_expiry_stored(self):
        c = Card(number="1234567890123456", expiry_date="12/28")
        assert c.expiry_date == "12/28"

    def test_short_number_raises(self):
        with pytest.raises(ValueError, match="16 digits"):
            Card(number="1234")

    def test_long_number_raises(self):
        with pytest.raises(ValueError, match="16 digits"):
            Card(number="12345678901234567")

    def test_non_digit_raises(self):
        with pytest.raises(ValueError, match="16 digits"):
            Card(number="123456789012345a")
