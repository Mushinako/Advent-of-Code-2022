# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import total_ordering
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .typings import Coord


@dataclass(frozen=True, kw_only=True)
class Map:
    data: list[list[int]]
    start: Coord
    end: Coord

    def __getitem__(self, coord: Coord) -> int:
        """"""
        r, c = coord
        return self.data[r][c]


@total_ordering
class AStarNode:
    """"""

    coord: Coord
    g: None | int
    h: int
    route: None | list[AStarNode]
    height: int

    def __init__(self, *, coord: Coord, h: int, height: int) -> None:
        self.coord = coord
        self.g = None
        self.h = h
        self.route = None
        self.height = height

    def __str__(self) -> str:
        return f"Node({self.coord}, height {self.height}, {self.g}+{self.h}={self.f})"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.coord)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, AStarNode):
            return self.f == __o.f
        return NotImplemented

    def __lt__(self, __o: object) -> bool:
        """"""
        if isinstance(__o, AStarNode):
            self_f = self.f
            o_f = __o.f
            if self_f is None:
                if o_f is None:
                    return self.coord < __o.coord
                else:
                    return False
            else:
                if o_f is None:
                    return True
                else:
                    return self_f < o_f
        return NotImplemented

    @property
    def f(self) -> None | int:
        if self.g is None:
            return None
        return self.g + self.h


class AStarBase(ABC):
    """"""

    map_: Map
    row_count: int
    col_count: int
    nodes_map: list[list[AStarNode]]
    nodes_heap: list[AStarNode]
    visited_nodes: set[AStarNode]

    @abstractmethod
    def __init__(self, map_: Map) -> None:
        ...

    def __getitem__(self, coord: Coord) -> AStarNode:
        """"""
        r, c = coord
        return self.nodes_map[r][c]

    @abstractmethod
    def run(self) -> list[AStarNode]:
        ...

    def get_neighbor_nodes(self, node: AStarNode) -> list[AStarNode]:
        """"""
        nodes: list[AStarNode] = []
        r, c = node.coord
        if r > 0:
            nodes.append(self.nodes_map[r - 1][c])
        if r < self.row_count - 1:
            nodes.append(self.nodes_map[r + 1][c])
        if c > 0:
            nodes.append(self.nodes_map[r][c - 1])
        if c < self.col_count - 1:
            nodes.append(self.nodes_map[r][c + 1])
        return nodes

    class NoRoute(Exception):
        message: str

        def __init__(self, message: str, *args: object) -> None:
            super().__init__(message, *args)
            self.message = message
