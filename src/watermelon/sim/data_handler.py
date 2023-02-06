import pandas as pd


class DataExtractor:
    def __init__(self, *args, **kwargs):
        self.data = pd.DataFrame(*args, **kwargs)
