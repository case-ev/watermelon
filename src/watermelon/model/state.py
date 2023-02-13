"""
watermelon.model.state
----------------------
Functionality for the state of the agent
"""

from typing import Tuple
import dataclasses

from watermelon.model.vertex import Vertex
from watermelon.model.actions import VertexAction


@dataclasses.dataclass
class AgentState:
    """State of an agent at an instant"""

    vertex: Vertex = None
    action: VertexAction = None
    _soc: float = 1
    current_action: int = 0
    action_time: float = 0
    finished_action: bool = False
    is_waiting: bool = False
    is_done: bool = False
    is_travelling: Tuple[bool, Vertex, Vertex] = (False, None, None)
    just_arrived: bool = False
    out_of_charge: bool = False
    overcharged: bool = False

    @property
    def soc(self):
        """State of charge of the battery"""
        return self._soc

    @soc.setter
    def soc(self, val):
        self._soc = val

    def copy(self):
        """Create a copy of itself"""
        return dataclasses.replace(self)
