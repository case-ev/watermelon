# Agents

## Agents and states
An agent is modelled by the `Agent` class, which contains:

- An identifier that, like with vertices, **must** be unique as the program associates a singleton to a specific identifier.
- The graph that the agent belongs to. Currently, the program doesn't use this information anywhere but, in the future, this might change so it is recommended to specify it anyways.
- A group of the decisions that the agent makes in the graph. These decisions are contained in the `Decision` data structure, which is essentially a tuple of vertices and actions intended to represent taking an action at a specific vertex.
- A state variable which represents the state of said agent at that moment. This is modelled by the `AgentState` data structure.
- A battery capacity in Wh, which indicates how much energy the battery holds.
- A material capacity in kg, which indicates how heavy of a payload the agent can carry.
- A model of the uncertainty involved in SOC estimation. The different models available and their functionality are specified in [Uncertainty models](#uncertainty-models).

The state corresponds to a dataclass which contains information about the current state of the agent. This information corresponds to the current vertex and action, the state of charge of the battery, the current payload, as well as status flags (is the agent finished, is it waiting, is it travelling, etc.). The following are all the attributes contained in the `AgentState` class:

- `vertex`: Vertex the agent is in.
- `action`: Action the agent is taking.
- `_soc`: True state of charge. This can be accessed and set through the `soc` property, which makes sure the other properties are properly changed.
- `payload`: Payload the agent is carrying.
- `current_action`: Index of the current action the agent is taking.
- `action_time`: Time the agent has taken to complete the current action.
- `finished_action`: Whether the agent has finished the current action.
- `is_waiting`: Whether the agent is waiting or not.
- `is_done`: Whether the agent has finished all tasks.
- `is_travelling`: Whether the agent is travelling.
- `just_arrived`: Whether the agent has just arrived to a vertex.
- `out_of_charge`: Whether the agent has ran out of charge.
- `overcharged`: Whether the agent's battery has been overcharged.

## State of charge
Even though the true state of charge (accessible through the state of the agent) is available, this is only for simulation purposes. In the real world, the true state of charge can not be known so it must be estimated: this estimation leads to uncertainty, which can be modelled in different ways.

In order to consider this uncertainty, users should use the `soc` property in the agent (not the one in the state), which takes into consideration the uncertainty model given when instancing the agent.
