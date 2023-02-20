# Graph creation and usage

## How to create a graph
To create a graph, you must first initialize the corresponding vertices and edges, which are created by `Vertex` and `Edge`, respectively.

For vertices, they each take:

- A unique identifier. This **must** be unique, since the program associates a singleton vertex for each identifier meaning that the following holds
```python
>>> v1 = wm.Vertex(1, **properties)
>>> v2 = wm.Vertex(1)
>>> v1 is v2
True
```
- The capacity of the vertex. If it is not given, it assumes the vertex has infinite capacity.
- The type of vertex. We will talk more about these, but they indicate the purpose of the vertex in the graph.

On the other hand, for edges each one takes:

- An origin and target vertex.
- An associated optional weight. This weight indicates the amount of energy in Wh that it takes to travel the edge in the graph.
- An optional time parameter, which indicates how long (in minutes) it takes to cross the edge.

Once you have created all the necessary vertices and edges, you can create a graph using `Graph`. You can choose to initialize it directly with the vertices and edges, or initialize an empty graph and add them later using the `add_vertex/add_vertices` and `add_edge/add_edges` methods, respectively.
