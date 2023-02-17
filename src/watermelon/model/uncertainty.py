"""
watermelon.model.uncertainty
----------------------------
Sources of uncertainty in the model.
"""

import abc

import numpy as np


class UncertaintySource(abc.ABC):
    """Abstract source of uncertainty"""

    @property
    @abc.abstractmethod
    def last(self):
        """Gets the last sample that was taken from the distribution"""

    @abc.abstractmethod
    def sample(self):
        """Get a sample of the distribution"""


class GaussianUncertainty(UncertaintySource):
    """Model for gaussian uncertainty"""

    def __init__(self, mean=0, std=0.001):
        self.mean = mean
        self.std = std
        self._last_sample = None

    @property
    def last(self):
        return self._last_sample

    def sample(self):
        value = np.random.default_rng().normal(self.mean, self.std)
        self._last_sample = value
        return value
