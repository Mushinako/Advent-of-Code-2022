# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = type(None)


class Solution(SolutionAbstract):
    day = 9
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 09 data.
        """

    def part_1(self) -> ...:
        """
        Day 09 part 1 solution.
        """

    def part_2(self) -> ...:
        """
        Day 09 part 2 solution.
        """
