"""
watermelon_solver.agent.decoder
-------------------------------
Decoder that turns a binary code into a list of actions that a given
agent takes.
"""

from typing import Iterable, Tuple

import watermelon as wm


class ActionDecoder:
    """Decoder for the actions of an agent"""

    def __call__(
        self, word: Iterable[bool]
    ) -> Iterable[Tuple[wm.Vertex, wm.VertexAction]]:
        return self.decode(word)

    def decode(
        self, word: Iterable[bool]
    ) -> Iterable[Tuple[wm.Vertex, wm.VertexAction]]:
        """Decode the given word into a list of actions"""
        # TODO: Figure out an encoding scheme for the actions
        # TODO: Implement decoding for the actions
