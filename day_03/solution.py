# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[str]


class Solution(SolutionAbstract):
    day = 3
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 03 data.
        """
        return raw_data

    def part_1(self) -> int:
        """
        Day 03 part 1 solution.
        """
        sum_ = 0
        for rucksack in self.data:
            item_count = len(rucksack)
            if item_count % 2:
                raise ValueError("Rucksack is not evenly sized")
            half_length = item_count // 2
            comp1 = rucksack[:half_length]
            comp2 = rucksack[half_length:]
            (common,) = set(comp1) & set(comp2)
            sum_ += self._to_priority(common)
        return sum_

    def part_2(self) -> int:
        """
        Day 03 part 2 solution.
        """
        sum_ = 0
        elf_count = len(self.data)
        if elf_count % 3:
            raise ValueError("Elf count is not divisible by 3")
        for i in range(0, elf_count, 3):
            elf1, elf2, elf3 = self.data[i : i + 3]
            (common,) = set(elf1) & set(elf2) & set(elf3)
            sum_ += self._to_priority(common)
        return sum_

    @staticmethod
    def _to_priority(letter: str) -> int:
        """"""
        if "A" <= letter <= "Z":
            return ord(letter) - 38
        if "a" <= letter <= "z":
            return ord(letter) - 96
        raise ValueError(f"Unknown priority letter: {letter}")
