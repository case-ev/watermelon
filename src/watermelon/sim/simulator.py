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

    def __init__(self, graph, agents, *, delta=1e-3, battery_eff=0.75):
        self.graph = graph
        self.agents = agents
        self.delta = delta
        self.time = 0.0
        self.state = np.array([a.actions[0] for a in agents])
        self.data_extractor = None
        self.battery_eff = battery_eff

    def start(self, extractor_cls=DataFrameExtractor):
        """Start the simulation. It must be ran before you start updating"""
        LOGGER.info("Starting simulation")
        self.data_extractor = extractor_cls(self)

    def update(self):
        """Update the simulation. Should be run at every timestep"""
        LOGGER.debug("Starting iteration")
        self.time += self.delta

        # State update code
        for agent in self.agents:
            agent.state.action_time += self.delta

            if not agent.state.is_done:
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
                        agent.state.action_time = 0
                        agent.state.soc -= edge.weight / (self.battery_eff * agent.battery_capacity)
                else:
                    # It is doing some action
                    if agent.state.just_arrived:
                        vertex.members.append(agent)
                        agent.state.is_waiting = True
                        agent.state.just_arrived = False

                    if agent.state.is_waiting:
                        agent.state.is_waiting = vertex.capacity < len(vertex.members)
                    else:
                        time, energy = action.act(agent, vertex)
                        if agent.state.action_time > time:
                            agent.state.finished_action = True
                            agent.state.soc -= energy / (self.battery_eff * agent.battery_capacity)

                # Go to the next action if appropiate
                if agent.state.finished_action:
                    # Send the agent to sleep if there are no more actions left
                    if agent.state.current_action + 1 >= len(agent.actions):
                        LOGGER.info("Agent finished")
                        agent.state.is_done = True
                        agent.state.action_time = 0
                    else:
                        next_vertex, _ = agent.actions[agent.state.current_action + 1].tuple()
                        if next_vertex is not vertex:
                            agent.state.is_travelling = (True, vertex, next_vertex)
                            agent.state.action_time = 0
                        agent.state.current_action += 1
                        agent.state.finished_action = False

        # Store the data
        LOGGER.debug("Storing iteration data")
        try:
            self.data_extractor.append(self)
        except Exception as e:
            LOGGER.error(
                "Failed to append data to the extractor. Did you forget to start the simulation?"
            )
            raise e
