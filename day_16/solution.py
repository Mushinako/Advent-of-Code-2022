# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cached_property
from itertools import permutations

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
        shortest_lengths = self.data.lengths_map

        def run(*, path: list[str], time: int, score: int, score_delta: int) -> int:
            """"""
            node = path[-1]
            possible_ends = [
                end
                for end, travel_time in shortest_lengths[node].items()
                if end not in path and travel_time < time
            ]
            # Wander around for the rest of the time
            max_score = score + time * score_delta
            # Go to another valve
            for end in possible_ends:
                travel_time = shortest_lengths[node][end]
                end_score = run(
                    path=path + [end],
                    time=time - travel_time - 1,
                    score=score + (travel_time + 1) * score_delta,
                    score_delta=score_delta + valves[end],
                )
                max_score = max(max_score, end_score)
            # Get max score
            return max_score

        return run(path=["AA"], time=30, score=0, score_delta=0)

    def part_2(self) -> int:
        """
        Day 16 part 2 solution.
        """
        valves = self.data.valves
        shortest_lengths = self.data.lengths_map

        # cache: dict[tuple[frozenset[_Player], int, int, int], int] = {}

        def run(
            *, p1: _Player, p2: _Player, time: int, score: int, score_delta: int
        ) -> int:
            """"""
            # key = (frozenset([p1, p2]), time, score, score_delta)
            # cached = cache.get(key)
            # if cached is not None:
            #     return cached

            print(f"Trying {p1=}; {p2=}; {time=}; {score=}; {score_delta=}")
            # Wander around for the rest of the time
            max_score = score + time * score_delta
            # P1 in waiting
            if p1.wait > 0:
                states1 = [(_Player(visited=p1.visited, wait=p1.wait - 1), 0)]
            # P1 needs new node
            else:
                node1 = p1.visited[-1]
                ends1 = [
                    end
                    for end, travel_time in shortest_lengths[node1].items()
                    if end not in p1.visited
                    and end not in p2.visited
                    and travel_time < time
                ]
                states1 = [
                    (
                        _Player(
                            visited=p1.visited + (end1,),
                            wait=shortest_lengths[node1][end1],
                        ),
                        valves[end1],
                    )
                    for end1 in ends1
                ]
            # P2 in waiting
            if p2.wait > 0:
                states2 = [(_Player(visited=p2.visited, wait=p2.wait - 1), 0)]
            # P2 needs new node
            else:
                node2 = p2.visited[-1]
                ends2 = [
                    end
                    for end, travel_time in shortest_lengths[node2].items()
                    if end not in p1.visited
                    and end not in p2.visited
                    and travel_time < time
                ]
                states2 = [
                    (
                        _Player(
                            visited=p2.visited + (end2,),
                            wait=shortest_lengths[node2][end2],
                        ),
                        valves[end2],
                    )
                    for end2 in ends2
                ]
            # Run
            for np1, ndelta1 in states1:
                for np2, ndelta2 in states2:
                    if np1.visited[-1] == np2.visited[-1]:
                        continue
                    end_score = run(
                        p1=np1,
                        p2=np2,
                        time=time - 1,
                        score=score + score_delta,
                        score_delta=score_delta + ndelta1 + ndelta2,
                    )
                    max_score = max(max_score, end_score)

            # cache[key] = max_score
            return max_score

        return run(
            p1=_Player(visited=("AA",), wait=0),
            p2=_Player(visited=("AA",), wait=0),
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

    @cached_property
    def lengths_map(self) -> dict[str, dict[str, int]]:
        """"""
        interesting_nodes = ["AA"] + list(self.valves)
        return {
            start: {
                end: nx.shortest_path_length(self.graph, source=start, target=end)
                for end in self.valves
                if start != end
            }
            for start in interesting_nodes
        }


@dataclass(frozen=True, kw_only=True)
class _Player:
    """"""

    visited: tuple[str, ...]
    wait: int

    def __hash__(self) -> int:
        return hash((self.visited, self.wait))
