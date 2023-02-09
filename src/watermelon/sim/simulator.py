"""
watermelon.sim.simulator
------------------------
Main functionality of the simulator, which takes a graph and a collection
of agents and runs the simulation given their decisions.
"""

import numpy as np

from watermelon_common.logger import LOGGER
from watermelon.sim.data_extractor import DataFrameExtractor


class Simulator:
    """Object that simulates the graph"""

    def __init__(self, graph, agents, *, delta=1e-3):
        self.graph = graph
        self.agents = agents
        self.delta = delta
        self.time = 0.0
        self.state = np.array([a.actions[0] for a in agents])
        self.data_extractor = None

    def start(self, extractor_cls=DataFrameExtractor):
        """Start the simulation. It must be ran before you start updating"""
        self.data_extractor = extractor_cls(self.agents, self.state)

    def update(self):
        """Update the simulation. Should be run at every timestep"""
        self.time += self.delta

        # State update code
        for agent in self.agents:
            decision = agent.actions[agent.current_action]

            # Go to the next action if appropiate
            if agent.finished_action:
                agent.current_action += 1
                agent.finished_action = False

        try:
            self.data_extractor.append(self)
        except Exception as e:
            LOGGER.error(
                "Failed to append data to the extractor. Did you forget to start the simulation?"
            )
            raise e
