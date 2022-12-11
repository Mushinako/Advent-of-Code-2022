# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[list[int]]
    _R = int
    _C = int
    _Coord = tuple[_R, _C]


class Solution(SolutionAbstract):
    day = 8
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 08 data.
        """
        return [list(map(int, list(r))) for row in raw_data if (r := row.strip())]

    def part_1(self) -> int:
        """
        Day 08 part 1 solution.
        """
        r_count = len(self.data)
        c_count = len(self.data[0])
        candidates: list[_Coord] = [
            (r, c) for r in range(1, r_count - 1) for c in range(1, c_count - 1)
        ]
        unseeable_count = 0

        for r, c in candidates:
            height = self.data[r][c]
            # From left
            trees_to_left = self.data[r][:c]
            if max(trees_to_left) < height:
                continue
            # From right
            trees_to_right = self.data[r][c + 1 :]
            if max(trees_to_right) < height:
                continue
            # From top
            trees_to_top = (row[c] for row in self.data[:r])
            if max(trees_to_top) < height:
                continue
            # From bottom
            trees_to_bottom = (row[c] for row in self.data[r + 1 :])
            if max(trees_to_bottom) < height:
                continue
            # Can't see
            unseeable_count += 1

        return r_count * c_count - unseeable_count

    def part_2(self) -> int:
        """
        Day 08 part 2 solution.
        """
        r_count = len(self.data)
        c_count = len(self.data[0])
        candidates: list[_Coord] = [
            (r, c) for r in range(1, r_count - 1) for c in range(1, c_count - 1)
        ]
        return max(self._get_scenic_score(r, c) for r, c in candidates)

    def _get_scenic_score(self, r: int, c: int) -> int:
        """"""
        height = self.data[r][c]
        # From left
        left_count = 0
        for tree_to_left in self.data[r][:c][::-1]:
            left_count += 1
            if tree_to_left >= height:
                break
        # From right
        right_count = 0
        for tree_to_right in self.data[r][c + 1 :]:
            right_count += 1
            if tree_to_right >= height:
                break
        # From top
        top_count = 0
        for tree_to_top in (row[c] for row in self.data[:r][::-1]):
            top_count += 1
            if tree_to_top >= height:
                break
        # From bottom
        bottom_count = 0
        for tree_to_bottom in (row[c] for row in self.data[r + 1 :]):
            bottom_count += 1
            if tree_to_bottom >= height:
                break
        # Calculate score
        return left_count * right_count * top_count * bottom_count
