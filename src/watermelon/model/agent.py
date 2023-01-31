class Agent:
    def __init__(self, graph, actions=None):
        self.graph = graph

        # Each element in `actions` is a 2-tuple of a vertex
        # and an action.
        if actions is None:
            self.actions = []
        else:
            self.actions = actions
