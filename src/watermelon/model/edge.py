"""
watermelon.model.edge
---------------------
Definition of edges in the graph, which connect two vertices.
"""


class Edge:
    """Edge connecting two vertices"""

    def __init__(self, origin, target, weight=None, time=None):
        self.origin = origin
        self.target = target
        self.weight = weight
        self.time = time

    def __eq__(self, __o):
        if not isinstance(__o, self.__class__):
            return False

        return (
            self.origin == __o.origin
            and self.target == __o.target
            and self.weight == __o.weight
            and self.time == __o.time
        )

    def __repr__(self):
        return f"Edge(origin={repr(self.origin)}, target={repr(self.target)}, \
weight={repr(self.weight)}, time={repr(self.time)})"

    def __str__(self):
        return f"({str(self.origin)}->{str(self.target)}; w={str(self.weight)}, t={str(self.time)})"
