from dataclasses import dataclass
from typing import List

import numpy as np

from .base import Bet, IndexedClass
from .constants import BET, LAY, UNMATCHED
from .events import Event


class Agent(IndexedClass):
    open_bets: List[Bet]

    def __init__(self, starting_capital: float):
        self.capital = starting_capital
        self.open_bets = list()
        super().__init__()

    def bet(self, event: Event, min_odds: float, stake: float) -> Bet:
        self.capital -= stake

        bet = Bet(
            limit_odds=min_odds, stake=stake, agent=self, event=event, bet_type=BET
        )

        self.open_bets.append(bet)
        event.bets.append((bet, UNMATCHED))

        return bet

    def lay(self, event: Event, max_odds: float, stake: float) -> Bet:
        self.capital -= stake

        bet = Bet(
            limit_odds=max_odds, stake=stake, agent=self, event=event, bet_type=LAY
        )

        self.open_bets.append(bet)
        event.lays.append((bet, UNMATCHED))

        return bet

    def __str__(self):
        lines = [f"**Agent {self.idx}**"]
        lines.append(f"  Capital: {self.capital:.2f}")
        lines.append("  Open bets:")
        for bet in self.open_bets:
            lines.append("    " + str(bet))

        return "\n".join(lines)
