from watermelon.model.state import AgentState


class Agent:
    def __init__(self, identifier, graph, initial_state=AgentState(), actions=None):
        self._id = identifier
        self._id_hash = hash(identifier)
        self.graph = graph
        self.state = initial_state

        # Each element in `actions` is a 2-tuple of a vertex
        # and an action.
        if actions is None:
            self.actions = []
        else:
            self.actions = actions

    def __hash__(self):
        return self.hash

    def __eq__(self, __o):
        return (
            hash(self) == hash(__o)
            and self.type == __o.type
            and isinstance(__o, self.__class__)
        )

    def __repr__(self):
        return f"Agent({repr(self.id)})"

    def __str__(self):
        return f"Agent({str(self.id)})"

    @property
    def id(self):
        return self._id

    @property
    def hash(self):
        return self._id_hash
