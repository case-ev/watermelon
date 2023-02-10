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
            agent.state.action_time += self.delta
            decision = agent.actions[agent.state.current_action]
            vertex, action = decision.tuple()

            if agent.state.is_travelling[0]:
                # It is travelling to a vertex
                _, origin, target = agent.state.is_travelling
                edge = self.graph.get_edge(origin, target)
                travel_time = edge.time
                if agent.state.action_time > travel_time:
                    agent.state.is_travelling = (False, None, None)
                    agent.state.just_arrived = True
            else:
                # It is doing some action
                # if agent.state.just_arrived:
                #     if vertex.capacity >=
                time, energy = action.act(agent, vertex)

            # Go to the next action if appropiate
            if agent.state.finished_action:
                next_vertex, next_action = agent.actions[agent.state.current_action + 1].tuple()
                if next_vertex is not vertex:
                    agent.state.is_travelling = (True, vertex, next_vertex)
                    agent.state.action_time = 0
                agent.state.current_action += 1
                agent.state.finished_action = False

        try:
            self.data_extractor.append(self)
        except Exception as e:
            LOGGER.error(
                "Failed to append data to the extractor. Did you forget to start the simulation?"
            )
            raise e
