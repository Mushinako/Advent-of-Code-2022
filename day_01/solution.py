# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[list[int]]


class Solution(SolutionAbstract):
    day = 1
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 01 data.
        """
        data: _Data = []
        elf_calories: list[int] = []
        for row in raw_data:
            if row := row.strip():
                elf_calories.append(int(row))
            else:
                data.append(elf_calories)
                elf_calories = []
        data.append(elf_calories)
        return [elf_calories for elf_calories in data if elf_calories]

    def part_1(self) -> int:
        """
        Day 01 part 1 solution.
        """
        return max(map(sum, self.data))

    def part_2(self) -> int:
        """
        Day 01 part 2 solution.
        """
        sums = sorted(map(sum, self.data))
        return sum(sums[-3:])
