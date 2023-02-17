"""
watermelon.model.state
----------------------
Functionality for the state of the agent
"""

from typing import Tuple
import dataclasses

from watermelon.model.actions import VertexAction
from watermelon.model.vertex import Vertex


@dataclasses.dataclass
class AgentState:
    """State of an agent at an instant"""

    vertex: Vertex = None
    action: VertexAction = None
    _soc: float = 1
    payload: float = 0
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
        """True state of charge. In reality this would be unobtainable, but it
        is left as available for simulation purposes.
        """
        return self._soc

    @soc.setter
    def soc(self, val):
        self._soc = val
        if self._soc <= 0:
            self._soc = 0
            self.out_of_charge = True
        elif self._soc > 1:
            self.overcharged = True
        else:
            self.out_of_charge = False
            self.overcharged = False

    def copy(self):
        """Create a copy of itself"""
        return dataclasses.replace(self)
