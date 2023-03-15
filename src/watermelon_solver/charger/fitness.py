"""
watermelon_solver.charger.fitness
----------------------------------
Code in charge of evaluating the given distribution of chargers in a graph.
"""

from typing import List

from watermelon_solver.agent.fitness import AgentFitness
from watermelon_solver.charger.encoding import GraphDecoder

import watermelon as wm
import genus


class GraphFitness:
    """Object for the fitness function of the given distribution of chargers in a graph"""

    def __init__(
        self,
        initial_costs: List[float],
        op_costs: List[float],
        agents: List[wm.Agent],
        graph: wm.Graph,
        agent_fitness: AgentFitness,
        l: float = 0.5,
        discount_rate: float = 0.08,
        *,
        decoder=None,
    ) -> None:
        self.initial_costs = initial_costs
        self.op_costs = op_costs
        self.agents = agents
        self._graph = graph
        self.agent_fitness = agent_fitness
        self.decoder = (
            GraphDecoder(self._graph) if decoder is None else decoder(self._graph)
        )
        self.l = l
        self.discount_rate = discount_rate

    def _cost(self, graph: wm.Graph) -> float:
        cost = 0
        for v in graph.vertices:
            is_charger = isinstance(v.type, wm.EVChargerType)
            vertex_cost = self.initial_costs[v] + self.op_costs[v] / self.discount_rate
            cost += vertex_cost * is_charger
        return cost

    def _time(self, graph: wm.Graph) -> float:
        # TODO: Implement evaluating time
        pass

    def evaluate(self, code: List[bool]) -> float:
        """Evaluate the given graph"""
        graph = self.decoder(code)
        return self.l * self._cost(graph) + (1.0 - self.l) * self._time(graph)

    def __call__(self, chrom: genus.Chromosome) -> float:
        return self.evaluate(chrom.code)
