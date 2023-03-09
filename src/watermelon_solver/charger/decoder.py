"""
watermelon_solver.charger.decoder
-------------------------------
Decoder that turns a binary code into a graph with chargers installed in tehe
appropiate locations.
"""

from typing import Iterable

import watermelon as wm


class ChargerDecoder:
    """Decoder for the locations of chargers"""

    def __call__(self, word: Iterable[bool]) -> wm.Graph:
        return self.decode(word)

    def decode(self, word: Iterable[bool]) -> wm.Graph:
        """Decode the given word into a graph with the given chargers"""
