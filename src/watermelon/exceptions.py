"""
watermelon.exceptions
---------------------
Different kinds of exceptions used in the program.
"""


class ForbiddenActionException(Exception):
    """Exception for a forbidden action"""

    def __init__(self, action, vertex_type):
        super().__init__(
            f"Action {action.__class__.__name__} not allowed \
in vertex type {vertex_type.__class__.__name__}"
        )


class NonExistentEdgeException(Exception):
    """Exception for a non existent edge in a graph"""

    def __init__(self, origin, target):
        super().__init__(f"Edge {origin}->{target} does not exist")
