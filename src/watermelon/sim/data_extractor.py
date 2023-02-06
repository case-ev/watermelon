import pandas as pd


class DataExtractor:
    def __init__(self, *args, **kwargs):
        self.data = pd.DataFrame(*args, **kwargs)

    def append(self, simulation_state):
        data = {
            **{"time": [simulation_state.time]},
            **{
                a: action
                for a, action in zip(simulation_state.agents, simulation_state.state)
            },
        }
        self.data = pd.concat([self.data, pd.DataFrame(data)], ignore_index=True)
