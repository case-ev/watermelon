"""
watermelon.model.state
----------------------
Functionality for the state of the agent
"""

import dataclasses

from watermelon.model.vertex import Vertex
from watermelon.model.actions import VertexAction


@dataclasses.dataclass
class AgentState:
    """State of an agent at an instant"""

    vertex: Vertex = None
    action: VertexAction = None
    soc: float = None
