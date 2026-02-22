from typing import List

from ..card_reader.card_retainer import CardRetainer
from session_manager import logger as log


class RetainedCardCollector:
    """Collects retained cards by technician."""

    def __init__(self, retainer: CardRetainer) -> None:
        self.retainer = retainer
        self.logger = log.Logger()

    def collect_retained(self) -> List[str]:
        """Get list of retained card numbers and clear bin."""
        retained = [card.number for card in self.retainer._retained]
        self.retainer._retained = []
        self.logger.info(f"Collected {len(retained)} retained cards")
        return retained
