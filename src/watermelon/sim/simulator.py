"""
watermelon.sim.simulator
------------------------
Main functionality of the simulator, which takes a graph and a collection
of agents and runs the simulation given their decisions.
"""

from typing import List

from watermelon_common.logger import LOGGER
from watermelon.defaults import BATTERY_EFFICIENCY
from watermelon import model
from watermelon.sim.data_extractor import DataFrameExtractor, SimulationDataExtractor


class SimulationParameters:
    """Parameters for the simulation"""

    def __init__(self, *, battery_eff: float = BATTERY_EFFICIENCY, **_) -> None:
        self.battery_eff = battery_eff


class SimulationControl:
    """Control variables for the simulation"""

    def __init__(
        self,
        *,
        time: float = 0.0,
        delta: float = 1e-3,
        iteration: int = 0,
        should_close: bool = False,
        stop_time: float = 0.0,
        data_extractor: SimulationDataExtractor = None,
        **_,
    ) -> None:
        self.time = time
        self.delta = delta
        self.iteration = iteration
        self.should_close = should_close
        self.stop_time = stop_time
        self.data_extractor = data_extractor


class Simulator:
    """Object that simulates the graph"""

    def __init__(
        self,
        graph: model.Graph,
        agents: List[model.Agent],
        control: SimulationControl = None,
        params: SimulationParameters = None,
        **kwargs,
    ) -> None:
        self.graph = graph
        self.agents = agents
        self.control = SimulationControl(**kwargs) if control is None else control
        self.params = SimulationParameters(**kwargs) if params is None else params

    @property
    def time(self) -> float:
        """Current time of the simulation"""
        return self.control.time

    @property
    def should_close(self) -> bool:
        """Control variable that indicates if the simulation should end"""
        return self.control.should_close

    @property
    def data_extractor(self) -> SimulationDataExtractor:
        """Extractor for the simulation data"""
        return self.control.data_extractor

    @data_extractor.setter
    def data_extractor(self, val: SimulationDataExtractor) -> None:
        self.control.data_extractor = val

    def start(
        self,
        stop_time: float,
        *,
        extractor_cls: SimulationDataExtractor = DataFrameExtractor,
    ) -> None:
        """Start the simulation. It must be ran before you start updating"""
        LOGGER.info("Starting simulation")
        self.control.data_extractor = extractor_cls(self)
        self.control.iteration = 0
        self.control.stop_time = stop_time
        self.control.should_close = False

    def update(self) -> None:
        """Update the simulation. Should be run at every timestep"""
        LOGGER.debug(
            "Iteration %i @ time %.2f", self.control.iteration, self.control.time
        )
        self.control.time += self.control.delta
        self.control.should_close = self.control.time >= self.control.stop_time
        self.control.iteration += 1

        # State update code
        finished_simulation = True
        for agent in self.agents:
            agent.state.action_time += self.control.delta
            finished_simulation &= agent.state.is_done

            if not (agent.state.is_done or agent.state.out_of_charge):
                self._update_agent(agent)
        self.control.should_close |= finished_simulation

        if self.control.should_close and not finished_simulation:
            LOGGER.warning("Reached stop time but some agents haven't finished")

        # Store the data
        try:
            self.control.data_extractor.append(self)
        except AttributeError:
            LOGGER.error(
                "Failed to append data to the extractor. Did you forget to start the simulation?"
            )
            self.control.should_close = True

    def _update_agent(self, agent: model.Agent) -> None:
        decision = agent.actions[agent.state.current_action]
        vertex, action = decision.tuple()
        self._do_action(agent, vertex, action)
        self._check_next_action(agent, vertex)

    def _do_action(
        self, agent: model.Agent, vertex: model.Vertex, action: model.VertexAction
    ) -> None:
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
                agent.insert_energy(-edge.weight, self.params.battery_eff)

        if not agent.state.is_travelling[0]:
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

            if not agent.state.is_waiting:
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
                    agent.insert_energy(energy, self.params.battery_eff)

    def _check_next_action(self, agent: model.Agent, vertex: model.Vertex) -> None:
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
