"""
watermelon_solver.charger_solver
-------------------------
Class that abstracts away the process of finding the optimal locations
of chargers in a given graph.
"""

from typing import List

import watermelon as wm


class ChargerSolver:
    """Class that finds the best locations for chargers in a graph"""

    def __call__(self, graph: wm.Graph) -> List[bool]:
        return self.solve(graph)

    def solve(self, graph: wm.Graph) -> List[bool]:
        """Find the best locations"""
