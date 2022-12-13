# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import networkx as nx

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import TypeAlias

    _R = int
    _C = int
    _Coord = tuple[_R, _C]

    _Data: TypeAlias = "_Map"


class Solution(SolutionAbstract):
    day = 12
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 12 data.
        """
        data: list[list[int]] = []
        start: None | _Coord = None
        end: None | _Coord = None
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

        return _Map(data=data, start=start, end=end)

    def part_1(self) -> int:
        """
        Day 12 part 1 solution.
        """
        DG = self._get_graph()
        return nx.shortest_path_length(DG, source=self.data.start, target=self.data.end)

    def part_2(self) -> int:
        """
        Day 12 part 2 solution.
        """
        DG = self._get_graph()
        lengths: dict[_Coord, int] = nx.shortest_path_length(DG, target=self.data.end)
        return min(length for (r, c), length in lengths.items() if self.data[r, c] == 1)

    def _get_graph(self) -> nx.DiGraph:
        """"""
        DG = nx.DiGraph()
        DG.add_nodes_from(
            (r, c)
            for r in range(len(self.data.data))
            for c in range(len(self.data.data[0]))
        )
        for r, row in enumerate(self.data.data):
            for c, cell in enumerate(row):
                max_h = cell + 1
                DG.add_edges_from(
                    ((r, c), (nr, nc))
                    for (nr, nc), nh in self.data.get_neighbors(r, c).items()
                    if nh <= max_h
                )
        return DG


@dataclass(frozen=True, kw_only=True)
class _Map:
    data: list[list[int]]
    start: _Coord
    end: _Coord

    def __getitem__(self, coord: _Coord) -> int:
        """"""
        r, c = coord
        return self.data[r][c]

    def get_neighbors(self, r: _R, c: _C) -> dict[_Coord, int]:
        """"""
        nodes_map: dict[_Coord, int] = {}
        if r > 0:
            nodes_map[r - 1, c] = self[r - 1, c]
        if r < len(self.data) - 1:
            nodes_map[r + 1, c] = self[r + 1, c]
        if c > 0:
            nodes_map[r, c - 1] = self[r, c - 1]
        if c < len(self.data[0]) - 1:
            nodes_map[r, c + 1] = self[r, c + 1]
        return nodes_map
