# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from heapq import heappop, heappush
from typing import TYPE_CHECKING

from .utils import AStarBase, AStarNode, Map

if TYPE_CHECKING:
    from .solution import Solution


def part_2(self: Solution) -> int:
    """"""

    a_star = _AStar(self.data)
    path = a_star.run()
    return len(path) - 1


class _AStar(AStarBase):
    """"""

    map_: Map
    row_count: int
    col_count: int
    nodes_map: list[list[AStarNode]]
    nodes_heap: list[AStarNode]
    visited_nodes: set[AStarNode]

    def __init__(self, map_: Map) -> None:
        self.map_ = map_
        self.row_count = len(map_.data)
        self.col_count = len(map_.data[0])
        er, ec = map_.end
        self.nodes_map = [
            [
                AStarNode(
                    coord=(r, c), h=abs(r - er) + abs(c - ec), height=self.map_[r, c]
                )
                for c in range(self.col_count)
            ]
            for r in range(self.row_count)
        ]
        self.nodes_heap = []
        self.visited_nodes = set()

    def run(self) -> list[AStarNode]:
        """"""
        start_node = self[self.map_.start]
        start_node.g = 0
        start_node.route = []
        self.nodes_heap.append(start_node)

        while self.nodes_heap:
            curr_node = heappop(self.nodes_heap)
            # print(f"Visiting node at {curr_node}...")
            if curr_node.g is None:
                raise ValueError("Missing `g` value")
            if curr_node.route is None:
                raise ValueError("Missing route")

            if curr_node.coord == self.map_.end:
                break

            self.visited_nodes.add(curr_node)
            max_height = self.map_[curr_node.coord] + 1
            next_nodes = [
                node
                for node in self.get_neighbor_nodes(curr_node)
                if node not in self.visited_nodes and node.height <= max_height
            ]

            g = curr_node.g + 1
            route = curr_node.route + [curr_node]
            for next_node in next_nodes:
                if next_node.g is not None and next_node.g <= g:
                    continue
                next_node.g = g
                next_node.route = route
                heappush(self.nodes_heap, next_node)
                self.visited_nodes.discard(next_node)

        end_node = self[self.map_.end]
        if end_node.route is None:
            raise self.NoRoute("No route found")
        return end_node.route + [end_node]
