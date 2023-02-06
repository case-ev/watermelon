class Agent:
    def __init__(self, identifier, graph, actions=None):
        self._id = identifier
        self._id_hash = hash(identifier)
        self.graph = graph

        # Each element in `actions` is a 2-tuple of a vertex
        # and an action.
        if actions is None:
            self.actions = []
        else:
            self.actions = actions

    @property
    def id(self):
        return self._id

    @property
    def hash(self):
        return self._id_hash
