import itertools
from collections import namedtuple


class IndexedClass:
    _idx_iter = itertools.count()

    def __init__(self):
        self.idx = next(self._idx_iter)


class Bet(namedtuple("Bet", ["bet_type", "limit_odds", "stake", "agent", "event"])):
    def __str__(self):
        return (
            f"{self.bet_type.capitalize()}("
            f"limit_odds={self.limit_odds}, "
            f"stake={self.stake}, "
            f"agent_idx={self.agent.idx}, "
            f"event_idx={self.event.idx})"
        )
