# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self

    _Data = list["_Round"]


class _RPS(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


@dataclass(frozen=True)
class _Round:
    opponent: _RPS
    you: str

    @classmethod
    def from_row(cls, opponent_str: str, you: str) -> Self:
        opponent = {"A": _RPS.ROCK, "B": _RPS.PAPER, "C": _RPS.SCISSORS}[opponent_str]
        return cls(opponent, you)

    def get_score_1(self) -> int:
        match self.you:
            case "X":
                return (
                    1 + {_RPS.ROCK: 3, _RPS.PAPER: 0, _RPS.SCISSORS: 6}[self.opponent]
                )
            case "Y":
                return (
                    2 + {_RPS.ROCK: 6, _RPS.PAPER: 3, _RPS.SCISSORS: 0}[self.opponent]
                )
            case "Z":
                return (
                    3 + {_RPS.ROCK: 0, _RPS.PAPER: 6, _RPS.SCISSORS: 3}[self.opponent]
                )
            case _:
                raise ValueError(f"Unknown action {self.you=}")

    def get_score_2(self) -> int:
        match self.you:
            case "X":
                return (
                    0 + {_RPS.ROCK: 3, _RPS.PAPER: 1, _RPS.SCISSORS: 2}[self.opponent]
                )
            case "Y":
                return (
                    3 + {_RPS.ROCK: 1, _RPS.PAPER: 2, _RPS.SCISSORS: 3}[self.opponent]
                )
            case "Z":
                return (
                    6 + {_RPS.ROCK: 2, _RPS.PAPER: 3, _RPS.SCISSORS: 1}[self.opponent]
                )
            case _:
                raise ValueError(f"Unknown action {self.you=}")


class Solution(SolutionAbstract):
    day = 2
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 02 data.
        """
        return [_Round.from_row(*line.split()) for line in raw_data]

    def part_1(self) -> int:
        """
        Day 02 part 1 solution.
        """
        return sum(round.get_score_1() for round in self.data)

    def part_2(self) -> int:
        """
        Day 02 part 2 solution.
        """
        return sum(round.get_score_2() for round in self.data)
