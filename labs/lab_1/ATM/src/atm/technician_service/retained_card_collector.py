"""Collection of retained cards by technician."""

from ..card_reader.card_retainer import CardRetainer
from ..session_manager.logger import Logger


class RetainedCardCollector:
    """Collects retained cards by technician."""

    def __init__(self, retainer: CardRetainer) -> None:
        """Store reference to card retainer."""
        self.retainer = retainer
        self.logger = Logger()

    def collect_retained(self) -> list[str]:
        """Return retained card numbers and clear retainer bin."""
        retained = [card.number for card in self.retainer._retained]
        self.retainer._retained = []
        self.logger.info(f"Collected {len(retained)} retained cards")
        return retained
