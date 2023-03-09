"""
watermelon_solver.agent_solver
-------------------------
Class that abstracts away the process of finding the optimal actions for a
group of agents.
"""

from typing import Dict, List

import watermelon as wm


class AgentSolver:
    """Class that finds the best actions that some agents can take"""

    def __call__(self, graph: wm.Graph) -> Dict[wm.Agent, List[wm.VertexAction]]:
        return self.solve(graph)

    def solve(self, graph: wm.Graph) -> Dict[wm.Agent, List[wm.VertexAction]]:
        """Find the best actions"""
