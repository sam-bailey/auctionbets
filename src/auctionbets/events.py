from collections import namedtuple
from typing import List, Optional, Tuple

import yaml

from .base import Bet, IndexedClass
from .constants import BET, LAY, MATCHED, SETTLED, UNMATCHED


class Event(IndexedClass):
    def __init__(self, true_probability):
        self.true_probability = true_probability

        self.bets: List[Tuple[Bet, str]] = list()
        self.lays: List[Tuple[Bet, str]] = list()

        self.is_matched = False
        self.is_settled = False
        self.bettor_odds: Optional[float] = None
        self.layer_odds: Optional[float] = None

        super().__init__()

    def __str__(self):
        lines = [f"**Event {self.idx}**"]
        lines.append(f"  True Probability: {self.true_probability}")
        lines.append(f"  Bettor Odds: {self.bettor_odds or 'unset'}")
        lines.append(f"  Layer Odds: {self.layer_odds or 'unset'}")
        lines.append("  All bets:")
        for bet, status in self.bets:
            lines.append(f"    {bet} ({status})")
        for bet, status in self.lays:
            lines.append(f"    {bet} ({status})")

        return "\n".join(lines)

    def match_bets(self) -> None:
        """NOT VALIDATED YET"""
        remaining_lays = sorted(
            map(lambda x: x[0], self.lays), key=lambda x: x.limit_odds, reverse=True
        )
        remaining_bets = sorted(
            map(lambda x: x[0], self.bets), key=lambda x: x.limit_odds
        )

        matched_lays = []
        matched_bets = []
        total_stake_bet = 0.0
        total_stake_layed = 0.0

        while (len(remaining_lays) > 1) | (len(remaining_bets) > 1):
            print("\nNew round")

            current_lay_odds = remaining_lays[0].limit_odds
            current_bet_odds = remaining_bets[0].limit_odds

            print(f"{total_stake_bet = }")
            print(f"{total_stake_layed = }")
            print(f"{current_bet_odds = }")
            print(f"{current_lay_odds = }")

            lay_needed = (
                total_stake_bet * current_bet_odds
                >= total_stake_layed / current_lay_odds
            )

            if lay_needed:
                print("Lay Needed")

                if len(remaining_lays) <= 1:
                    print("Out of lays")
                    break

                next_lay_odds = remaining_lays[1].limit_odds
                print(f"{next_lay_odds = }")
                if next_lay_odds >= current_bet_odds:
                    print("Lay matched")
                    newly_matched_lay = remaining_lays.pop(0)
                    matched_lays.append(newly_matched_lay)
                    total_stake_layed += newly_matched_lay.stake
                else:
                    print("Match not possible")
                    break

            else:
                print("Bet Needed")
                if len(remaining_bets) <= 1:
                    print("Out of bets")
                    break

                next_bet_odds = remaining_bets[1].limit_odds
                if next_bet_odds < current_lay_odds:
                    print("Bet matched")
                    newly_matched_bet = remaining_bets.pop(0)
                    matched_bets.append(newly_matched_bet)
                    total_stake_bet += newly_matched_bet.stake
                else:
                    print("Match not possible")
                    break

        print("Process complete")
        self.bets = [(_b, MATCHED) for _b in matched_bets] + [
            (_b, UNMATCHED) for _b in remaining_bets
        ]
        self.lays = [(_b, MATCHED) for _b in matched_lays] + [
            (_b, UNMATCHED) for _b in remaining_lays
        ]
        self.bettor_odds = current_bet_odds
        self.layer_odds = current_lay_odds

    def resolve_event(self, force_win: bool = False, force_lose: bool = False) -> None:
        pass

    # def run_auction(self) -> None:
    #     pass
    # if not self.is_complete:
    #     raise RuntimeError("Trying to collect an incomplete bet")

    # if not self.is_matched:
    #     stake_to_return = self.stake
    # elif self.is_winner:
    #     if self.bet_type == BET:
    #         stake_to_return = (1.0 + self.actual_odds)*self.stake
    #     elif self.bet_type == LAY:
    #         stake_to_return = (1.0 + 1.0 / self.actual_odds)*self.stake
    #     else:
    #         raise RuntimeError("Bet type should always be BET or LAY")
    # else:
    #     stake_to_return = 0.0

    # self.is_collected = True
    # return stake_to_return
