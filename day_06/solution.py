# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = str


class Solution(SolutionAbstract):
    day = 6
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 06 data.
        """
        return raw_data[0].strip()

    def part_1(self) -> int:
        """
        Day 06 part 1 solution.
        """
        return self._find_unique_substr_index(4)

    def part_2(self) -> int:
        """
        Day 06 part 2 solution.
        """
        return self._find_unique_substr_index(14)

    def _find_unique_substr_index(self, length: int) -> int:
        """"""
        for i in range(length, len(self.data)):
            if len(set(self.data[i - length : i])) == length:
                return i
        raise ValueError("No answer found")
