Agents - Watermelon

---

## Agents and states
An agent is modelled by the `Agent` class, which contains:
- An identifier that, like with vertices, **must** be unique as the program associates a singleton to a specific identifier.
- The graph that the agent belongs to. Currently, the program doesn't use this information anywhere but, in the future, this might change so it is recommended to specify it anyways.
- A group of the decisions that the agent makes in the graph. These decisions are contained in the `Decision` data structure, which is essentially a tuple of vertices and actions intended to represent taking an action at a specific vertex.
- A state variable which represents the state of said agent at that moment. This is modelled by the `AgentState` data structure.
- A battery capacity in Wh, which indicates how much energy the battery holds.
- A material capacity in kg, which indicates how heavy of a payload the agent can carry.

The state corresponds to a dataclass which contains information about the current state of the agent. This information corresponds to the current vertex and action, the state of charge of the battery, the current payload, as well as status flags (is the agent finished, is it waiting, is it travelling, etc.). The following are all the attributes contained in the `AgentState` class:
-
