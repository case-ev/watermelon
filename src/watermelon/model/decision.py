"""
watermelon.model.decision
-------------------------
Decision structure, which contains a vertex and an action.
"""

import dataclasses

from watermelon.model.actions import VertexAction
from watermelon.model.vertex import Vertex


@dataclasses.dataclass
class Decision:
    """Decision containing an action and a tuple"""

    vertex: Vertex
    action: VertexAction

    def __str__(self) -> str:
        return f"({str(self.vertex)}, {str(self.action)})"

    def tuple(self) -> tuple:
        """Parse into a tuple"""
        return self.vertex, self.action
