from atm.card_reader.card import Card
from atm.card_reader.card_retainer import CardRetainer


class TestCardRetainer:
    def test_retain_and_list(self):
        r = CardRetainer()
        c = Card(number="1234567890123456")
        r.retain(c)
        assert len(r._retained) == 1
        assert r._retained[0].number == "1234567890123456"
