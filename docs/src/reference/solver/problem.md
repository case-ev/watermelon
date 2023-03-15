# Optimization problem

The optimization problem that *watermelon* tries to solve is made of two parts:
- First, for a given distribution of chargers we need to find the sequence of decisions that the agents must take in order to minimize some statistic of the total time.
- Having the mechanism to find the optimal decisions, we find the distribution of chargers that maximizes the "utility".

## Agent Routing Problem (ARP)

For the ARP, the mathematical formulation is

\\[
    \min_{\delta^{(1)}, \dots, \delta^{(M)}} \mathcal{T}\left(\left.\delta^{(1)}, \dots, \delta^{(M)}\right|\mathbf{x}\right)
\\]
where \\(\mathcal{T}: S(\mathcal{V}\times A)\rightarrow \mathbb{R}\\) is some statistic of the time it takes for all agents, with \\(S(\mathcal{V}\times A)\\) the space of all sequences of a vertex-action tuple. A basic statistic consists of a cumulative statistic \\(\mathcal{T}_{\mathrm{c}}\\) such that

\\[
    \mathcal{T}_{\mathrm{c}}\left(\left.\delta^{(1)}, \dots, \delta^{(M)}\right|\mathbf{x}\right) = \sum _{\xi_i\in\Xi}T\left(\delta^{(i)}\right)
\\]
with \\(\Xi\\) the set of all agents.

## Charger Location Problem (CLP)

On the other hand, for the CLP the formulation is

\\[
    \max_{\mathbf{x}\in\\{0, 1\\}^{|V|}} \lambda C(\mathbf{x}) + (1 - \lambda)T(\mathbf{x})
\\]
where \\(C(\cdot)\\) is the cost function, \\(T(\cdot)\\) is the time function, and \\(\lambda\\) is a hyperparameter to balance between prioritizing costs or times.

### Modelling costs

The proposed cost function is of the form
\\[
    C(\mathbf{x}) = \sum_{n\geq 0}\frac{\mathbf{c}_n^{\mathrm{T}}\mathbf{x}}{\left(1 + r\right)^{n}}
\\]
where \\(\mathbf{c}_n\in\mathbb{R}^{|V|}\\) refers to the cost at period \\(n\\), such that each of its components indicates the cost of a specific vertex. \\(r\\) is a discount rate, which is used to project future costs to the present.

Assuming that there are only two unique costs, an initial cost \\(\mathbf{c}_0\\) and an operation cost \\(\mathbf{c}\\), the cost function can be expressed as
\\[
    C(\mathbf{x}) = \left(\mathbf{c}_0 + \frac{\mathbf{c}}{r}\right)^{\mathrm{T}}\mathbf{x}
\\]

### Modelling times

In order to model the penalization of times, it is necessary to solve the ARP and extract the best solution out of it. This solution for some charger distribution \\(\mathbf{x}\\) is passed back to the statistic, and its additive inverse is then used as the reward.

Formalizing this, suppose the sequences \\(d^{(1)}, \dots, d^{(M)}\\) are the solution to the ARP for some distribution \\(\mathbf{x}\\). Then, the time reward is defined as
\\[
    T(\mathbf{x}) = -\mathcal{T}\left(\left.d^{(1)}, \dots, d^{(M)}\right|\mathbf{x}\right)
\\]
with \\(\mathcal{T}\\) the same statistic that was chosen in the ARP.
