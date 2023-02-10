"""
watermelon.model.vertex_types
-----------------------------
Types of vertices
"""

import abc

import watermelon.model.actions as actions


class VertexType(abc.ABC):
    """Base interface for a node type"""

    @staticmethod
    @abc.abstractmethod
    def _char():
        pass

    @property
    @abc.abstractmethod
    def capacity(self):
        """Maximum capacity of the vertex"""

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, __o):
        return self.__class__ is __o.__class__

    @classmethod
    def __str__(cls):
        return cls._char()


class EmptyVertexType(VertexType):
    """Empty node"""

    ACTIONS = [actions.NullAction(), actions.WaitAction()]

    @staticmethod
    def _char():
        return "\u03b8"  # theta

    @property
    def capacity(self):
        return float("inf")


class EVChargerType(VertexType):
    """Charger for electric vehicles"""

    ACTIONS = [actions.ChargeBatteryAction(), actions.NullAction(), actions.WaitAction()]

    def __init__(self, capacity, charge_power):
        self._capacity = capacity
        self._charge_power = charge_power

    @staticmethod
    def _char():
        return "EV"

    @property
    def capacity(self):
        return self._capacity
