from watermelon.sim.data_handler import DataExtractor
import numpy as np


class Simulator:
    def __init__(self, graph, agents, delta=1e-3):
        self.graph = graph
        self.agents = agents
        self.data_handler = None
        self.delta = delta
        self.time = 0.0
        self.state = np.array([[a.actions[0] for a in agents]])

    def start(self):
        self.data_handler = DataExtractor(
            data={
                **{"time": [0]},
                **{a: action for a, action in zip(self.agents, self.state[0])},
            }
        )

    def update(self):
        self.time += self.delta
