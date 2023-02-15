Vertex types and actions - Watermelon

---

## Types & actions
The idea behind the simulation of the graphs is that each vertex contains one (and only one) type, which indicates its functionality in the simulated reality. These types then allow specific actions, depending on the type.

Each vertex and each action have a unique symbol associated to them, mostly for visualization purposes.

The currently implemented vertex types are:

- `EmptyVertexType` (θ): Vertex that is not of a specific type, but rather a "structural" member.
- `EVChargerType` (C): Charger for an electric vehicle.
- `MaterialLoadType` (X): Point where material is loaded.
- `MaterialDischargeType` (O): Point where material is depositted.

The currently implemented actions are:

- `NullAction` (ϕ): Doing nothing.
- `ChargeBatteryAction` (c): Charging the battery of the vehicle.
- `WaitAction` (w): Waiting for some time.
- `LoadMaterialAction` (x): Loading material.
- `DischargeMaterialAction` (o): Depositting material in the vertex.

As said previously, the allowed actions depend on the type of the current vertex. The mapping between each type and the actions it allows is the following:

- `EmptyVertexType`: ϕ, w
- `EVChargerType`: ϕ, w, c
- `MaterialLoadType`: ϕ, w, x
- `MaterialDischargeType`: ϕ, w, o

To add a new type, create a class that inherits from `VertexType` and implements the `\_char()` static method, which returns the unique character associated to that vertex type. It also has to contain a class attribute called `ACTIONS`, which corresponds to a list containing all the allowed actions.
