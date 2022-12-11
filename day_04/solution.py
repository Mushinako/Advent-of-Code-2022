# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Range = tuple[int, int]
    _Data = list[tuple[_Range, _Range]]


class Solution(SolutionAbstract):
    day = 4
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 04 data.
        """
        data: _Data = []
        for row in raw_data:
            elf1_str, elf2_str = row.split(",")
            elf1_start, elf1_end = map(int, elf1_str.split("-"))
            elf2_start, elf2_end = map(int, elf2_str.split("-"))
            data.append(((elf1_start, elf1_end), (elf2_start, elf2_end)))
        return data

    def part_1(self) -> int:
        """
        Day 04 part 1 solution.
        """
        count = 0
        for (elf1_start, elf1_end), (elf2_start, elf2_end) in self.data:
            if elf1_start <= elf2_start and elf2_end <= elf1_end:
                count += 1
                continue
            if elf2_start <= elf1_start and elf1_end <= elf2_end:
                count += 1
                continue
        return count

    def part_2(self) -> int:
        """
        Day 04 part 2 solution.
        """
        count = 0
        for (elf1_start, elf1_end), (elf2_start, elf2_end) in self.data:
            if elf1_start <= elf2_start <= elf1_end:
                count += 1
                continue
            if elf1_start <= elf2_end <= elf1_end:
                count += 1
                continue
            if elf2_start <= elf1_start <= elf2_end:
                count += 1
                continue
            if elf2_start <= elf1_end <= elf2_end:
                count += 1
                continue
        return count
