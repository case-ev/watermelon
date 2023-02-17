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
    def last(self) -> float:
        """Gets the last sample that was taken from the distribution"""

    @abc.abstractmethod
    def sample(self) -> float:
        """Get a sample of the distribution"""


class NoUncertainty(UncertaintySource):
    """Model for a deterministic output"""

    def __init__(self) -> None:
        self._last_sample = 0

    @property
    def last(self) -> float:
        return self._last_sample

    def sample(self) -> float:
        return 0


class GaussianUncertainty(UncertaintySource):
    """Model for gaussian uncertainty"""

    def __init__(self, mean: float = 0, std: float = 0.001) -> None:
        self.mean = mean
        self.std = std
        self._last_sample = None

    @property
    def last(self) -> float:
        return self._last_sample

    def sample(self) -> float:
        value = np.random.default_rng().normal(self.mean, self.std)
        self._last_sample = value
        return value
