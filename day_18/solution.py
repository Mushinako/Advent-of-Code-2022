# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

import networkx as nx

from utils import SolutionAbstract

if TYPE_CHECKING:
    from collections.abc import Generator

    _X = int
    _Y = int
    _Z = int
    _Coord = tuple[_X, _Y, _Z]
    _Data = list[_Coord]


class Solution(SolutionAbstract):
    day = 18
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 18 data.
        """
        return [tuple(map(int, line.split(","))) for line in raw_data]

    def part_1(self) -> int:
        """
        Day 18 part 1 solution.
        """
        droplets_set = set(self.data)
        total_faces = 6 * len(self.data)
        for coord in self.data:
            for neighbor_coord in self._get_neighbors(coord):
                total_faces -= neighbor_coord in droplets_set
        return total_faces

    def part_2(self) -> int:
        """
        Day 18 part 2 solution.
        """
        all_faces = self.part_1()
        droplets_set = set(self.data)

        x_min = min(x for x, _, _ in self.data)
        x_max = max(x for x, _, _ in self.data)
        y_min = min(y for _, y, _ in self.data)
        y_max = max(y for _, y, _ in self.data)
        z_min = min(z for _, _, z in self.data)
        z_max = max(z for _, _, z in self.data)

        all_air_coords = {
            coord
            for x in range(x_min - 1, x_max + 2)
            for y in range(y_min - 1, y_max + 2)
            for z in range(z_min - 1, z_max + 2)
            if (coord := (x, y, z)) not in droplets_set
        }
        G = nx.Graph()
        G.add_nodes_from(all_air_coords)
        for coord in all_air_coords:
            G.add_edges_from(
                [
                    (coord, neighbor_coord)
                    for neighbor_coord in self._get_neighbors(coord)
                    if neighbor_coord in all_air_coords
                ]
            )

        target_coord = (x_min - 1, y_min - 1, z_min - 1)
        print(f"X range: {x_min} ~ {x_max}")
        print(f"Y range: {y_min} ~ {y_max}")
        print(f"Z range: {z_min} ~ {z_max}")
        for airx in range(x_min, x_max + 1):
            for airy in range(y_min, y_max + 1):
                for airz in range(z_min, z_max + 1):
                    air_coord = (airx, airy, airz)
                    # Not air block
                    if air_coord in droplets_set:
                        continue
                    # Can reach outside
                    if nx.has_path(G, air_coord, target_coord):
                        continue
                    # Found inside air. Remove all faces touching
                    print(f"  Found inside air at {air_coord}")
                    for neighbor_coord in self._get_neighbors(air_coord):
                        all_faces -= neighbor_coord in droplets_set

        return all_faces

    @staticmethod
    def _get_neighbors(coord: _Coord) -> Generator[_Coord, None, None]:
        """"""
        x, y, z = coord
        yield (x - 1, y, z)
        yield (x + 1, y, z)
        yield (x, y - 1, z)
        yield (x, y + 1, z)
        yield (x, y, z - 1)
        yield (x, y, z + 1)
