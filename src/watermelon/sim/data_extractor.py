import pandas as pd


class DataFrameExtractor:
    def __init__(self, agents, initial_state):
        self.data = pd.DataFrame(self.parse_data(agents, initial_state, 0))

    def append(self, simulation_state):
        data = self.parse_data(
            simulation_state.agents, simulation_state.state, simulation_state.time
        )
        self.data = pd.concat([self.data, pd.DataFrame(data)], ignore_index=True)

    @staticmethod
    def parse_data(agents, state, time=0):
        return {
            **{"time": [time]},
            **{a: action for a, action in zip(agents, state)},
        }
