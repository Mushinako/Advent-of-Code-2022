# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cache
from itertools import permutations
from typing import TYPE_CHECKING

import networkx as nx
from matplotlib import pyplot as plt

from utils import SolutionAbstract

_LINE_RE = re.compile(
    r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)$"
)


class Solution(SolutionAbstract):
    day = 16
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 16 data.
        """
        G = nx.DiGraph()
        tunnels: list[tuple[str, str]] = []
        valves: dict[str, int] = {}
        for line in raw_data:
            match = _LINE_RE.fullmatch(line)
            if match is None:
                raise ValueError("Invalid input line")
            node = match[1]
            rate = int(match[2])
            neighbors = [n.strip() for n in match[3].split(",")]
            G.add_node(node)
            if rate > 0:
                valves[node] = rate
            tunnels.extend((node, neighbor) for neighbor in neighbors)
        G.add_edges_from(tunnels)
        return _Data(graph=G, valves=valves)

    def part_1(self) -> int:
        """
        Day 16 part 1 solution.
        """
        valves = self.data.valves
        interesting_nodes = ["AA"] + list(valves)
        shortest_lengths: dict[tuple[str, str], int] = {
            (start, end): nx.shortest_path_length(
                self.data.graph, source=start, target=end
            )
            for start, end in permutations(interesting_nodes, 2)
        }

        def run(
            *, path: list[str], node: str, time: int, score: int, score_delta: int
        ) -> int:
            """"""
            possible_ends = [
                end
                for (start, end), travel_time in shortest_lengths.items()
                if start == node and end not in path and travel_time < time
            ]
            # Wander around for the rest of the time
            max_score = score + time * score_delta
            # Go to another valve
            for end in possible_ends:
                travel_time = shortest_lengths[node, end]
                end_score = run(
                    path=path + [end],
                    node=end,
                    time=time - travel_time - 1,
                    score=score + (travel_time + 1) * score_delta,
                    score_delta=score_delta + valves[end],
                )
                max_score = max(max_score, end_score)
            # Get max score
            return max_score

        return run(path=["AA"], node="AA", time=30, score=0, score_delta=0)

    def part_2(self) -> int:
        """
        Day 16 part 2 solution.
        """
        valves = self.data.valves
        interesting_nodes = ["AA"] + list(valves)
        shortest_lengths: dict[tuple[str, str], int] = {
            (start, end): nx.shortest_path_length(
                self.data.graph, source=start, target=end
            )
            for start, end in permutations(interesting_nodes, 2)
        }

        cache: dict[tuple[frozenset[_Player], int, int, int], int] = {}

        def run(
            *, p1: _Player, p2: _Player, time: int, score: int, score_delta: int
        ) -> int:
            """"""
            key = (frozenset([p1, p2]), time, score, score_delta)
            cached = cache.get(key)
            if cached is not None:
                return cached

            # print(f"Trying {p1=}; {p2=}; {time=}; {score=}; {score_delta=}")
            # Wander around for the rest of the time
            max_score = score + time * score_delta
            # P1 in waiting
            if p1.wait > 0:
                states1 = [
                    (_Player(visited=p1.visited, node=p1.node, wait=p1.wait - 1), 0)
                ]
            # P1 needs new node
            else:
                ends1 = [
                    end
                    for (start, end), travel_time in shortest_lengths.items()
                    if start == p1.node
                    and end not in p1.visited
                    and end not in p2.visited
                    and travel_time < time
                ]
                states1 = [
                    (
                        _Player(
                            visited=p1.visited | {end1},
                            node=end1,
                            wait=shortest_lengths[p1.node, end1],
                        ),
                        valves[end1],
                    )
                    for end1 in ends1
                ]
            # P2 in waiting
            if p2.wait > 0:
                states2 = [
                    (_Player(visited=p2.visited, node=p2.node, wait=p2.wait - 1), 0)
                ]
            # P2 needs new node
            else:
                ends2 = [
                    end
                    for (start, end), travel_time in shortest_lengths.items()
                    if start == p2.node
                    and end not in p1.visited
                    and end not in p2.visited
                    and travel_time < time
                ]
                states2 = [
                    (
                        _Player(
                            visited=p2.visited | {end2},
                            node=end2,
                            wait=shortest_lengths[p2.node, end2],
                        ),
                        valves[end2],
                    )
                    for end2 in ends2
                ]
            # Run
            for np1, ndelta1 in states1:
                for np2, ndelta2 in states2:
                    if np1.node == np2.node:
                        continue
                    end_score = run(
                        p1=np1,
                        p2=np2,
                        time=time - 1,
                        score=score + score_delta,
                        score_delta=score_delta + ndelta1 + ndelta2,
                    )
                    max_score = max(max_score, end_score)

            cache[key] = max_score
            return max_score

        return run(
            p1=_Player(visited=frozenset(["AA"]), node="AA", wait=0),
            p2=_Player(visited=frozenset(["AA"]), node="AA", wait=0),
            time=26,
            score=0,
            score_delta=0,
        )

    def draw_graph(self) -> None:
        """"""
        G = self.data.graph
        fig, ax = plt.subplots(nrows=1, ncols=1)
        nx.draw(
            G,
            ax=ax,
            with_labels=True,
            pos=nx.spring_layout(G, k=0.15, iterations=20),
        )
        fig.savefig("graph.png")


@dataclass(frozen=True, kw_only=True)
class _Data:
    graph: nx.DiGraph
    valves: dict[str, int]


@dataclass(frozen=True, kw_only=True)
class _Player:
    """"""

    visited: frozenset[str]
    node: str
    wait: int

    def __hash__(self) -> int:
        return hash((self.visited, self.node, self.wait))
