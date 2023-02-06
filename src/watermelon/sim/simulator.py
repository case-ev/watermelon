from watermelon.sim.data_extractor import DataExtractor
import numpy as np


class Simulator:
    def __init__(self, graph, agents, delta=1e-3):
        self.graph = graph
        self.agents = agents
        self.data_handler = None
        self.delta = delta
        self.time = 0.0
        self.state = np.array([a.actions[0] for a in agents])

    def start(self, extractor_cls=DataExtractor):
        self.data_extractor = extractor_cls(
            data={
                **{"time": [0]},
                **{a: action for a, action in zip(self.agents, self.state)},
            }
        )

    def update(self):
        self.time += self.delta

        # State update code ...

        self.data_extractor.append(self)
