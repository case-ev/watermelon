"""
watermelon_solver.agent.fitness
----------------------------------
Code in charge of evaluating the given decisions on a graph.
"""

from typing import List, Callable, Tuple

import numpy as np

from watermelon_solver.agent.encoding import ActionDecoder
from watermelon_common.logger import LOGGER

import watermelon as wm
import genus


MINIMUM_REWARD = -np.inf


def _get_times(*decisions, graph, sim):
    sim.graph = graph
    for a, d in zip(sim.agents, decisions):
        if d.vertex not in graph:
            return None
        a.actions = d
    sim.start()
    while not sim.should_close:
        sim.update()

    times = {a: None for a in sim.data_extractor.data}
    finished = {a: False for a in sim.data_extractor.data}

    # This code is coupled with the data extractor
    # TODO: Figure out a better way to extract data from each simulation
    for row in sim.data_extractor.data.iloc[::-1].iloc:
        for a, data in row.items()[1:]:
            if times[a] is not None:
                # Go to the next agent if we already found this
                # solution
                break

            # Inmediately give the minimum reward if an agent runs
            # out of charge
            if data.state.out_of_charge:
                return None
            if not data.is_done and finished[a]:
                times[a] = row["time"]
    return times


def _arithmetic_statistic(*decisions, graph, sim):
    return _cumulative_statistic(*decisions, graph=graph, sim=sim) / len(decisions)


def _cumulative_statistic(*decisions, graph, sim):
    times = _get_times(*decisions, graph=graph, sim=sim)
    if times is None:
        return MINIMUM_REWARD

    total_time = 0
    for t in times.values():
        total_time += t
    return -total_time


class AgentFitness:
    """Object for the fitness function of the actions of agents in a graph"""

    def __init__(
        self,
        agents: List[wm.Agent] = None,
        *,
        decoder=None,
        stat: Callable[[*Tuple[wm.Vertex, wm.VertexAction], wm.Graph, wm.sim.Simulator], float]
        | str = None,
        **kwargs,
    ) -> None:
        self._agents = agents
        self.decoder = ActionDecoder() if decoder is None else decoder()
        self.sim = wm.sim.Simulator(None, self._agents, **kwargs)
        self._sim_kwargs = kwargs

        if isinstance(stat, str):
            match stat:
                case "c" | "cum" | "cumulative":
                    self.statistic = _cumulative_statistic
                case "a" | "ar" | "arithmetic":
                    self.statistic = _arithmetic_statistic
                case _:
                    self.statistic = _cumulative_statistic
                    LOGGER.warning(
                        "Could not interpret statistic %s, defaulting to cumulative statistic",
                        repr(stat),
                    )

        else:
            self.statistic = stat if stat is not None else _cumulative_statistic

    @property
    def agents(self):
        """Agents in the graph"""
        return self._agents

    @agents.setter
    def agents(self, val):
        self._agents = val
        self.sim = wm.sim.Simulator(None, val, **self._sim_kwargs)

    def evaluate(self, code: List[bool], graph: wm.Graph) -> float:
        """Evaluate the given actions"""
        decisions = self.decoder(code)
        return self.statistic(*decisions, graph=graph, sim=self.sim)

    def __call__(self, chrom: genus.Chromosome, graph: wm.Graph) -> float:
        return self.evaluate(chrom.code, graph)
