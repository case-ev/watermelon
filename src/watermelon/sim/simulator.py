"""
watermelon.sim.simulator
------------------------
Main functionality of the simulator, which takes a graph and a collection
of agents and runs the simulation given their decisions.
"""

import numpy as np

from watermelon_common.logger import LOGGER
from watermelon.defaults import BATTERY_EFFICIENCY
from watermelon.sim.data_extractor import DataFrameExtractor


class Simulator:
    """Object that simulates the graph"""

    def __init__(self, graph, agents, *, delta=1e-3, battery_eff=BATTERY_EFFICIENCY):
        self.graph = graph
        self.agents = agents
        self.delta = delta
        self.time = 0.0
        self.state = np.array([a.actions[0] for a in agents])
        self.data_extractor = None
        self.battery_eff = battery_eff
        self._iteration_num = 0
        self.should_close = False
        self.stop_time = 0

    def start(self, stop_time, *, extractor_cls=DataFrameExtractor):
        """Start the simulation. It must be ran before you start updating"""
        LOGGER.info("Starting simulation")
        self.data_extractor = extractor_cls(self)
        self._iteration_num = 0
        self.stop_time = stop_time
        self.should_close = False

    def update(self):
        """Update the simulation. Should be run at every timestep"""
        LOGGER.debug("Iteration %i", self._iteration_num)
        self.time += self.delta
        self.should_close = self.time >= self.stop_time
        self._iteration_num += 1

        # State update code
        finished_simulation = True
        for agent in self.agents:
            agent.state.action_time += self.delta
            finished_simulation &= agent.state.is_done

            if not (agent.state.is_done or agent.state.out_of_charge):
                self._update_agent(agent)
        self.should_close |= finished_simulation

        if self.should_close and not finished_simulation:
            LOGGER.warning("Reached stop time but some agents haven't finished")

        # Store the data
        try:
            self.data_extractor.append(self)
        except AttributeError:
            LOGGER.error(
                "Failed to append data to the extractor. Did you forget to start the simulation?"
            )
            self.should_close = True

    def _update_agent(self, agent):
        decision = agent.actions[agent.state.current_action]
        vertex, action = decision.tuple()
        self._do_action(agent, vertex, action)
        self._check_next_action(agent, vertex)

    def _do_action(self, agent, vertex, action):
        if agent.state.is_travelling[0]:
            # It is travelling to a vertex
            _, origin, target = agent.state.is_travelling
            edge = self.graph.get_edge(origin, target)
            travel_time = edge.time
            completion = (
                agent.state.action_time / travel_time if travel_time != 0 else 1
            )
            LOGGER.debug(
                "(%s|%i) %s->%s [%d%%]",
                agent,
                agent.state.current_action,
                origin,
                target,
                100 * completion,
            )
            if agent.state.action_time > travel_time:
                agent.state.is_travelling = (False, None, None)
                agent.state.just_arrived = True
                agent.state.action_time = 0
                self._update_soc(
                    agent, -edge.weight / (self.battery_eff * agent.battery_capacity)
                )
        else:
            # It is doing some action
            if agent.state.just_arrived:
                vertex.members.add(agent)
                agent.state.is_waiting = True
                agent.state.just_arrived = False

            if agent.state.is_waiting:
                LOGGER.debug(
                    "(%s|%i) waiting in %s", agent, agent.state.current_action, vertex
                )
                agent.state.is_waiting = vertex.capacity < len(vertex.members)
                if not agent.state.is_waiting:
                    # This would happen when the agent stops waiting and acts
                    agent.state.action_time = 0
            else:
                time, energy = action.act(agent, vertex)
                completion = agent.state.action_time / time if time != 0 else 1
                LOGGER.debug(
                    "(%s|%i) %s in %s [%d%%]",
                    agent,
                    agent.state.current_action,
                    action,
                    vertex,
                    100 * completion,
                )
                if agent.state.action_time > time:
                    vertex.members.discard(agent)
                    agent.state.finished_action = True
                    self._update_soc(
                        agent, energy / (self.battery_eff * agent.battery_capacity)
                    )

    def _check_next_action(self, agent, vertex):
        if agent.state.finished_action:
            # Send the agent to sleep if there are no more actions left
            if agent.state.current_action + 1 >= len(agent.actions):
                LOGGER.info("Agent %s finished", agent)
                agent.state.is_done = True
                agent.state.action_time = 0
            else:
                next_vertex, _ = agent.actions[agent.state.current_action + 1].tuple()
                if next_vertex is not vertex:
                    agent.state.is_travelling = (True, vertex, next_vertex)
                    agent.state.action_time = 0
                agent.state.current_action += 1
                agent.state.finished_action = False

    def _update_soc(self, agent, soc_delta):
        prev_soc = agent.state.soc
        agent.state.soc += soc_delta
        if agent.state.soc <= 0:
            agent.state.soc = 0
            agent.state.out_of_charge = True
        elif agent.state.soc > 1:
            agent.state.overcharged = True
        else:
            agent.state.out_of_charge = False
            agent.state.overcharged = False

        if agent.state.out_of_charge and prev_soc != 0:
            LOGGER.warning("%s ran out of charge", agent)
