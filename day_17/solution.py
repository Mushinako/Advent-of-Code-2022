# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from dataclasses import dataclass
from itertools import cycle
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Coord = complex  # Bottom is 0+0j to 6+0j
    _Data = list[str]


class Solution(SolutionAbstract):
    day = 17
    data: _Data

    _ROCKS = [
        [0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j],
        [1 + 0j, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j],
        [0 + 0j, 1 + 0j, 2 + 0j, 2 + 1j, 2 + 2j],
        [0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j],
        [0 + 0j, 1 + 0j, 0 + 1j, 1 + 1j],
    ]

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 17 data.
        """
        (line,) = raw_data
        return list(line)

    def part_1(self) -> int:
        """
        Day 17 part 1 solution.
        """
        return self._get_height_after_stones(2022)

    def part_2(self) -> int:
        """
        Day 17 part 2 solution.
        """
        map_: set[_Coord] = set()
        rock_patterns = cycle(self._ROCKS)
        movements = cycle(self.data)
        movement_len = len(self.data)
        # Make linter happy
        has_rock_moving = True
        rock = self._create_rock(pattern=next(rock_patterns), map_=map_)
        # Cycle vars
        last_past_10_rows: None | set[_Coord] = None
        last_rock_count = 0
        last_movement_index = 0
        last_movement_height = 0
        rock_count = 0
        movement_count = 0
        while True:
            if not has_rock_moving:
                pattern = next(rock_patterns)
                if pattern == self._ROCKS[0]:
                    movement_height = self._get_max_height(map_)
                    if movement_height > 500:  # Educated guess
                        movement_index = movement_count % movement_len
                        past_10_rows = {
                            coord - movement_height * 1j
                            for coord in map_
                            if movement_height - 10 <= coord.imag <= movement_height
                        }
                        if last_past_10_rows is None:
                            last_past_10_rows = past_10_rows
                            last_rock_count = rock_count
                            last_movement_index = movement_index
                            last_movement_height = movement_height
                        elif (
                            last_movement_index == movement_index
                            and last_past_10_rows == past_10_rows
                        ):
                            stone_cycle = rock_count - last_rock_count
                            height_cycle = movement_height - last_movement_height
                            break
                rock = self._create_rock(pattern=pattern, map_=map_)
                has_rock_moving = True
            match next(movements):
                case "<":
                    rock.move_left(map_)
                case ">":
                    rock.move_right(map_)
                case move:
                    raise ValueError(f"Invalid movement: {move}")
            movement_count += 1
            stopped = rock.move_down(map_)
            if stopped:
                has_rock_moving = False
                map_.update(rock.coords)
                rock_count += 1

        print(f"{stone_cycle=} {height_cycle=}")
        target = 1_000_000_000_000
        cycle_count, cycle_remainder = divmod(target, stone_cycle)
        return cycle_count * height_cycle + self._get_height_after_stones(
            cycle_remainder
        )

    def _get_height_after_stones(self, n: int) -> int:
        """"""
        map_: set[_Coord] = set()
        rock_patterns = cycle(self._ROCKS)
        movements = cycle(self.data)
        # Make linter happy
        has_rock_moving = True
        rock = self._create_rock(pattern=next(rock_patterns), map_=map_)
        rock_count = 0
        while rock_count < n:
            if not has_rock_moving:
                rock = self._create_rock(pattern=next(rock_patterns), map_=map_)
                has_rock_moving = True
            match next(movements):
                case "<":
                    rock.move_left(map_)
                case ">":
                    rock.move_right(map_)
                case move:
                    raise ValueError(f"Invalid movement: {move}")
            stopped = rock.move_down(map_)
            if stopped:
                has_rock_moving = False
                map_.update(rock.coords)
                rock_count += 1

        # self._print_space(map_=map_, rock=rock)
        return int(max(coord.imag for coord in map_) + 1)

    @staticmethod
    def _get_max_height(map_: set[_Coord]) -> int:
        """"""
        if not map_:
            return -1
        else:
            return int(max(coord.imag for coord in map_))

    @staticmethod
    def _create_rock(*, pattern: list[_Coord], map_: set[_Coord]) -> _Rock:
        """"""
        max_height = Solution._get_max_height(map_)
        return _Rock(pattern=pattern, base_coord=2 + (max_height + 4) * 1j)

    @staticmethod
    def _print_space(*, map_: set[_Coord], rock: _Rock) -> None:
        """"""
        max_height = Solution._get_max_height(map_)
        space = [["."] * 7 for _ in range(max_height + 8)]
        for coord in rock.coords:
            space[int(coord.imag)][int(coord.real)] = "+"
        for coord in map_:
            space[int(coord.imag)][int(coord.real)] = "#"
        for i, row in reversed(list(enumerate(space))):
            print(f"{i:>4}|{''.join(row)}|")
        print("    +-------+")


@dataclass(kw_only=True)
class _Rock:
    """"""

    pattern: list[_Coord]
    base_coord: _Coord

    @property
    def coords(self) -> list[_Coord]:
        return [coord + self.base_coord for coord in self.pattern]

    def move_left(self, map_: set[_Coord]) -> None:
        """"""
        new_base_coord = self.base_coord - 1
        for coord in self.pattern:
            new_coord = coord + new_base_coord
            if new_coord in map_ or new_coord.real < 0:
                break
        else:
            self.base_coord = new_base_coord

    def move_right(self, map_: set[_Coord]) -> None:
        """"""
        new_base_coord = self.base_coord + 1
        for coord in self.pattern:
            new_coord = coord + new_base_coord
            if new_coord in map_ or new_coord.real > 6:
                break
        else:
            self.base_coord = new_base_coord

    def move_down(self, map_: set[_Coord]) -> bool:
        """
        Returns:
            (bool) Whether the rock stopped
        """
        new_base_coord = self.base_coord - 1j
        for coord in self.pattern:
            new_coord = coord + new_base_coord
            if new_coord in map_ or new_coord.imag < 0:
                return True

        self.base_coord = new_base_coord
        return False
