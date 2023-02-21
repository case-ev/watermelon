# State of Charge & Uncertainty

## Uncertainty models
Since in the real world the State of Charge (SoC) of a battery can not be exactly known, it must be estimated. This estimation leads to errors which must be taken into consideration to develop a more robust model: thus, *watermelon* allows the user to specify some model for the uncertainty in the estimation of the SoC.

Uncertainty is modelled by some random variable \\(n(t)\\), such that, if \\(S_{\mathrm{C}}(t)\\) corresponds to the true SoC at time \\(t\in\mathbb{R}^+\\), then the estimated SoC is given by

\\[ \widehat S_{\mathrm{C}}(t) = S_{\mathrm{C}}(t) + n(t) \\]

Different models for \\(n(t)\\) can be defined, all of which inherit from the base class `UncertaintySource` and must implement the `last()` and `sample()` methods, which give the last sample and generate a new sample, respectively. The ones currently implemented in *watermelon* are:

- `NoUncertainty`: This means the estimation is perfect and has no error, meaning \\(\forall t, n(t) = 0\\).
- `GaussianUncertainty`: In this model, \\(n(t)\sim\operatorname{N}\left(\mu, \sigma^2\right)\\), where typically \\(\mu = 0\\). In this case, \\(\sigma\\) is associated to the level of uncertainty in the measurement, and the real SoC can be further estimated through some other statistical technique (such as Kalman filtering).
