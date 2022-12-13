# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

from .part_1 import part_1
from .part_2 import part_2
from .utils import Map

if TYPE_CHECKING:
    from .typings import C, Coord, R

    _Data = Map


class Solution(SolutionAbstract):
    day = 12
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 12 data.
        """
        data: list[list[int]] = []
        start: None | Coord = None
        end: None | Coord = None
        for r, row in enumerate(raw_data):
            row_int: list[int] = []
            for c, cell in enumerate(row):
                match cell:
                    case "S":
                        start = (r, c)
                        cell = "a"
                    case "E":
                        end = (r, c)
                        cell = "z"
                    case _:
                        pass
                row_int.append(ord(cell) - 96)
            data.append(row_int)

        if start is None:
            raise ValueError("No starting position found")
        if end is None:
            raise ValueError("No ending position found")

        return Map(data=data, start=start, end=end)

    def part_1(self) -> int:
        """
        Day 12 part 1 solution.
        """
        return part_1(self)

    def part_2(self) -> int:
        """
        Day 12 part 2 solution.
        """
        return part_2(self)
