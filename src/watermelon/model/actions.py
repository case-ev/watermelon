"""
watermelon.model.vertex_actions
-------------------------------
Types of actions that the agents can take
"""

import abc

from watermelon_common.logger import LOGGER
from watermelon.defaults import BATTERY_EFFICIENCY, LEAKAGE_POWER
from watermelon.exceptions import ForbiddenActionException


_MINUTES_PER_HOUR = 60


class VertexAction(abc.ABC):
    """Type of action"""

    @staticmethod
    @abc.abstractmethod
    def _char():
        """Unique character that represents an action"""

    @abc.abstractmethod
    def _act(self, agent, vertex):
        """Take an action in a vertex"""

    def act(self, agent, vertex):
        """Make an agent take this action on a vertex.

        This method returns both the time it takes to do the action and
        the amount of energy required to do it.

        Parameters
        ----------
        agent : watermelon.model.Agent
            Agent that takes the action
        vertex : watermelon.model.Vertex
            Vertex to add to the graph

        Returns
        -------
        time, energy : (float, float)
            Amount of time and energy that it takes to do the action
        """
        if self.__class__ not in vertex.type.ACTIONS:
            raise ForbiddenActionException(self, vertex.type)
        return self._act(agent, vertex)

    @classmethod
    def __repr__(cls):
        return cls.__class__.__name__

    @classmethod
    def __str__(cls):
        return cls._char()


class NullAction(VertexAction):
    """Action for not doing anything"""

    @staticmethod
    def _char():
        return "\u03d5"  # phi

    def _act(self, agent, vertex):
        return 0, 0


class ChargeBatteryAction(VertexAction):
    """Action for charging the battery"""

    def __init__(self, limit=0.8, battery_eff=BATTERY_EFFICIENCY):
        """Charge the battery.

        The specified battery efficiency indicates which percentage of
        the energy given by the battery is used as mechanical work to
        travel the graph.

        Parameters
        ----------
        limit : float, optional
            State of charged to be reached, by default 0.8
        battery_eff : float, optional
            Efficiency of the battery, by default BATTERY_EFFICIENCY
        """
        self.limit = limit
        self.battery_eff = battery_eff

    @staticmethod
    def _char():
        return "c"

    def _act(self, agent, vertex):
        if agent.soc >= self.limit:
            return 0, 0
        energy = (
            (self.limit - agent.soc) * self.battery_eff * agent.battery_capacity
        )
        time = _MINUTES_PER_HOUR * energy / vertex.type.charge_power
        LOGGER.info(
            "%s charging %.0f Wh (%.0f minutes) at %s", agent, energy, time, vertex
        )
        return time, energy


class WaitAction(VertexAction):
    """Action for waiting"""

    def __init__(self, time=0):
        """Wait for the given amount of time"""
        self.time = time

    @staticmethod
    def _char():
        return "w"

    def _act(self, agent, vertex):
        energy = LEAKAGE_POWER * self.time / _MINUTES_PER_HOUR
        return self.time, -energy


class LoadMaterialAction(VertexAction):
    """Action for loading material"""

    def __init__(self, limit=1, material=None):
        """Make the agent load material.

        Parameters
        ----------
        limit : float, 0 <= limit <= 1, optional
            Payload limit as a proportion, by default 1
        material : float, optional
            Amount of material to be loaded in kg, by default None. If
            it is specified, it overrides the value given by limit.
        """
        self.limit = limit
        self.material = material

    @staticmethod
    def _char():
        return "x"

    def _act(self, agent, vertex):
        if agent.state.payload >= self.limit:
            return 0, 0
        if self.material is None:
            material = (self.limit - agent.state.payload) * agent.material_capacity
        else:
            material = self.material
        time = material / vertex.type.load_rate

        leakage_energy = LEAKAGE_POWER * time / _MINUTES_PER_HOUR
        action_energy = 0
        energy = leakage_energy + action_energy
        LOGGER.info(
            "%s Loading %.0f kg (%.0f Wh, %.0f minutes) at %s",
            agent,
            material,
            energy,
            time,
            vertex,
        )
        return time, -energy


class DischargeMaterialAction(VertexAction):
    """Action for discharging material"""

    def __init__(self, limit=0, material=None):
        """Make the agent discharge material.

        Parameters
        ----------
        limit : float, 0 <= limit <= 1, optional
            Payload limit as a proportion, by default 1
        material : float, optional
            Amount of material to be discharged in kg, by default None. If
            it is specified, it overrides the value given by limit.
        """
        self.limit = limit
        self.material = material

    @staticmethod
    def _char():
        return "o"

    def _act(self, agent, vertex):
        if agent.state.payload <= self.limit:
            return 0, 0
        if self.material is None:
            material = (agent.state.payload - self.limit) * agent.material_capacity
        else:
            material = self.material
        time = material / vertex.type.load_rate

        leakage_energy = LEAKAGE_POWER * time / _MINUTES_PER_HOUR
        action_energy = 0
        energy = leakage_energy + action_energy
        LOGGER.info(
            "%s Discharging %.0f kg (%.0f Wh, %.0f minutes) at %s",
            agent,
            material,
            energy,
            time,
            vertex,
        )
        return time, -energy
