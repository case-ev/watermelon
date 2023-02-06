class Decision:
    def __init__(self, vertex, action):
        self.vertex = vertex
        self.action = action

    def __repr__(self):
        return f"Decision({repr(self.vertex)}, {repr(self.action)})"

    def __str__(self):
        return f"({str(self.vertex)}, {str(self.action)})"


class VertexAction:
    @classmethod
    def __repr__(cls):
        return cls.__class__.__name__

    @classmethod
    def __str__(cls):
        return cls._char()


class __NullAction(VertexAction):
    @staticmethod
    def _char():
        return "\u03d5"  # phi


NULL_ACTION = __NullAction()
