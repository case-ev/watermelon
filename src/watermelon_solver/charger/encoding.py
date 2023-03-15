"""
watermelon_solver.charger.encoding
-------------------------------
Encoder and decoder for the code representing the locations of chargers in
a graph.
"""

from typing import Iterable

import watermelon as wm


class GraphDecoder:
    """Decoder for the locations of chargers"""

    def __init__(self, graph: wm.Graph) -> None:
        self.graph = graph

    def __call__(self, code: Iterable[bool]) -> wm.Graph:
        return self.decode(code)

    def decode(self, code: Iterable[bool]) -> wm.Graph:
        """Decode the given code into a graph with the given chargers"""
        # TODO: Implement decoding for the charger locations
